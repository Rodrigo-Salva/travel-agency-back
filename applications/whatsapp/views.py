import requests
from django.conf import settings
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WhatsAppAccount, WhatsAppContact, WhatsAppConversation, WhatsAppMessage, WhatsAppCampaign
from .serializers import (
    WhatsAppConversationSerializer,
    WhatsAppMessageSerializer,
    WhatsAppContactSerializer,
    WhatsAppCampaignSerializer,
    SendMessageSerializer,
)


def waha_headers():
    key = settings.WAHA_API_KEY
    return {'X-Api-Key': key} if key else {}


def broadcast_to_admin(event_type, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'whatsapp_admin',
        {'type': 'whatsapp_event', 'data': {'type': event_type, **data}},
    )


def get_or_create_conversation(phone, name=''):
    contact, _ = WhatsAppContact.objects.get_or_create(
        phone=phone,
        defaults={'name': name},
    )
    owner_phone = WhatsAppAccount.get_active_phone()
    conversation, created = WhatsAppConversation.objects.get_or_create(contact=contact)
    if created or (owner_phone and not conversation.owner_phone):
        conversation.owner_phone = owner_phone
        conversation.save(update_fields=['owner_phone'])
    return conversation


class WAHAWebhookView(APIView):
    """Recibe eventos de WAHA: mensajes entrantes y confirmaciones de entrega."""
    permission_classes = [AllowAny]

    def post(self, request):
        event = request.data.get('event')
        payload = request.data.get('payload', {})

        if event == 'message':
            self._handle_incoming(payload)
        elif event == 'message.ack':
            self._handle_ack(payload)

        return Response({'ok': True})

    def _handle_incoming(self, payload):
        from_number = payload.get('from', '')
        body = payload.get('body', '')
        waha_id = payload.get('id', '')
        push_name = payload.get('_data', {}).get('notifyName', '')

        if not from_number or not body:
            return

        # waha_id puede venir como objeto dict en algunas versiones de WAHA
        if isinstance(waha_id, dict):
            waha_id = waha_id.get('_serialized') or waha_id.get('id') or ''

        conversation = get_or_create_conversation(from_number, push_name)

        # Deduplicar: si ya existe el mensaje con este waha_id, no crear otro
        if waha_id and WhatsAppMessage.objects.filter(waha_message_id=waha_id).exists():
            return

        conversation.last_message_at = timezone.now()
        conversation.unread_count += 1
        conversation.save()

        msg = WhatsAppMessage.objects.create(
            conversation=conversation,
            direction=WhatsAppMessage.DIRECTION_INCOMING,
            content=body,
            status=WhatsAppMessage.STATUS_DELIVERED,
            waha_message_id=waha_id,
        )

        broadcast_to_admin('message.received', {
            'messageId': msg.id,
            'conversationId': conversation.id,
            'contactPhone': conversation.contact.phone,
            'contactName': conversation.contact.name,
            'content': body,
            'direction': 'incoming',
            'createdAt': msg.created_at.isoformat(),
        })

    def _handle_ack(self, payload):
        raw_id = payload.get('id', '')
        # WAHA puede enviar el id como objeto {_serialized, id, fromMe, ...} o como string
        if isinstance(raw_id, dict):
            waha_id = raw_id.get('_serialized') or raw_id.get('id') or ''
        else:
            waha_id = str(raw_id) if raw_id else ''

        ack = payload.get('ack', 0)
        status_map = {1: 'sent', 2: 'delivered', 3: 'read', -1: 'failed'}
        new_status = status_map.get(int(ack) if ack else 0)
        if not new_status or not waha_id:
            return

        updated = WhatsAppMessage.objects.filter(waha_message_id=waha_id).update(status=new_status)
        if updated:
            msg = WhatsAppMessage.objects.get(waha_message_id=waha_id)
            broadcast_to_admin('message.status', {
                'messageId': msg.id,
                'status': new_status,
                'conversationId': msg.conversation_id,
            })


class DeliveryCallbackView(APIView):
    """Recibe notificaciones del microservicio Node.js cuando un job termina."""
    permission_classes = [AllowAny]

    def post(self, request):
        message_id = request.data.get('messageId')
        job_status = request.data.get('status')
        campaign_id = request.data.get('campaignId')
        # wahaMessageId puede venir como objeto desde WAHA — extraer string
        raw_id = request.data.get('wahaMessageId')
        if isinstance(raw_id, dict):
            waha_message_id = raw_id.get('_serialized') or raw_id.get('id') or str(raw_id)
        else:
            waha_message_id = raw_id

        if campaign_id:
            WhatsAppCampaign.objects.filter(id=campaign_id).update(status=job_status)
            broadcast_to_admin('campaign.status', {'campaignId': campaign_id, 'status': job_status})

        if message_id:
            update_data = {'status': job_status}
            if job_status == 'sent':
                update_data['sent_at'] = timezone.now()
            if waha_message_id:
                update_data['waha_message_id'] = waha_message_id

            WhatsAppMessage.objects.filter(id=message_id).update(**update_data)
            broadcast_to_admin('message.status', {'messageId': message_id, 'status': job_status})

        return Response({'ok': True})


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WhatsAppConversationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        owner_phone = WhatsAppAccount.get_active_phone()
        qs = WhatsAppConversation.objects.select_related('contact').all()
        if owner_phone:
            qs = qs.filter(owner_phone=owner_phone)
        return qs

    @action(detail=True, methods=['get'], url_path='messages')
    def messages(self, request, pk=None):
        conversation = self.get_object()
        conversation.unread_count = 0
        conversation.save(update_fields=['unread_count'])
        msgs = conversation.messages.all()
        serializer = WhatsAppMessageSerializer(msgs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='clear')
    def clear(self, request, pk=None):
        conversation = self.get_object()
        deleted, _ = conversation.messages.all().delete()
        conversation.unread_count = 0
        conversation.last_message_at = None
        conversation.save(update_fields=['unread_count', 'last_message_at'])
        return Response({'deleted': deleted})


class SendMessageView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        conversation = get_or_create_conversation(data['chat_id'])
        conversation.last_message_at = timezone.now()
        conversation.save(update_fields=['last_message_at'])

        scheduled_at = None
        if data['delay_ms'] > 0:
            from datetime import timedelta
            scheduled_at = timezone.now() + timedelta(milliseconds=data['delay_ms'])

        msg = WhatsAppMessage.objects.create(
            conversation=conversation,
            direction=WhatsAppMessage.DIRECTION_OUTGOING,
            content=data['content'],
            status=WhatsAppMessage.STATUS_PENDING,
            scheduled_at=scheduled_at,
        )

        try:
            resp = requests.post(
                f"{settings.WHATSAPP_SERVICE_URL}/api/queue/message",
                json={
                    'chatId': data['chat_id'],
                    'text': data['content'],
                    'messageId': msg.id,
                    'delayMs': data['delay_ms'],
                    'priority': data['priority'],
                },
                timeout=10,
            )
            resp.raise_for_status()
            job_id = resp.json().get('jobId')
            msg.status = WhatsAppMessage.STATUS_QUEUED
            msg.job_id = job_id
            msg.save(update_fields=['status', 'job_id'])
        except Exception as exc:
            msg.status = WhatsAppMessage.STATUS_FAILED
            msg.save(update_fields=['status'])
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        broadcast_to_admin('message.queued', {
            'messageId': msg.id,
            'conversationId': conversation.id,
            'content': data['content'],
            'direction': 'outgoing',
            'status': msg.status,
            'scheduledAt': scheduled_at.isoformat() if scheduled_at else None,
            'createdAt': msg.created_at.isoformat(),
        })

        return Response(WhatsAppMessageSerializer(msg).data, status=status.HTTP_201_CREATED)


class CancelMessageView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk=None):
        try:
            msg = WhatsAppMessage.objects.get(pk=pk)
        except WhatsAppMessage.DoesNotExist:
            return Response({'error': 'Mensaje no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        if not msg.job_id:
            return Response({'error': 'Este mensaje no tiene job asociado'}, status=status.HTTP_400_BAD_REQUEST)

        if msg.status not in [WhatsAppMessage.STATUS_QUEUED, WhatsAppMessage.STATUS_PENDING]:
            return Response({'error': f'No se puede cancelar: estado {msg.status}'}, status=status.HTTP_409_CONFLICT)

        try:
            resp = requests.delete(
                f"{settings.WHATSAPP_SERVICE_URL}/api/queue/cancel/{msg.job_id}",
                timeout=10,
            )
            resp.raise_for_status()
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        msg.status = WhatsAppMessage.STATUS_CANCELLED
        msg.save(update_fields=['status'])

        broadcast_to_admin('message.status', {'messageId': msg.id, 'status': 'cancelled'})
        return Response({'cancelled': True})


class WhatsAppCampaignViewSet(viewsets.ModelViewSet):
    queryset = WhatsAppCampaign.objects.prefetch_related('contacts').all()
    serializer_class = WhatsAppCampaignSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def launch(self, request, pk=None):
        campaign = self.get_object()

        if campaign.status not in [WhatsAppCampaign.STATUS_DRAFT, WhatsAppCampaign.STATUS_PAUSED]:
            return Response({'error': 'Solo se pueden lanzar campañas en estado borrador o pausada'}, status=status.HTTP_400_BAD_REQUEST)

        contacts_payload = [
            {'chatId': c.phone, 'messageId': None}
            for c in campaign.contacts.all()
        ]

        if not contacts_payload:
            return Response({'error': 'La campaña no tiene contactos'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear mensajes en DB para cada contacto
        messages_payload = []
        for contact in campaign.contacts.all():
            conversation = get_or_create_conversation(contact.phone)
            msg = WhatsAppMessage.objects.create(
                conversation=conversation,
                direction=WhatsAppMessage.DIRECTION_OUTGOING,
                content=campaign.message_template,
                status=WhatsAppMessage.STATUS_PENDING,
            )
            messages_payload.append({'chatId': contact.phone, 'messageId': msg.id})

        try:
            resp = requests.post(
                f"{settings.WHATSAPP_SERVICE_URL}/api/queue/campaign",
                json={
                    'campaignId': campaign.id,
                    'contacts': messages_payload,
                    'messageTemplate': campaign.message_template,
                    'delayBetweenMs': campaign.delay_between_ms,
                },
                timeout=10,
            )
            resp.raise_for_status()
            job_id = resp.json().get('jobId')
            campaign.status = WhatsAppCampaign.STATUS_RUNNING
            campaign.job_id = job_id
            campaign.save(update_fields=['status', 'job_id'])
        except Exception as exc:
            campaign.status = WhatsAppCampaign.STATUS_FAILED
            campaign.save(update_fields=['status'])
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(WhatsAppCampaignSerializer(campaign).data)


class QueueStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            resp = requests.get(f"{settings.WHATSAPP_SERVICE_URL}/api/queue/stats", timeout=5)
            resp.raise_for_status()
            return Response(resp.json())
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)


# ─── WAHA Session Management ───────────────────────────────────────────────────

class SessionStatusView(APIView):
    """Estado actual de la sesión WhatsApp — consulta la lista y busca la sesión."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            # Primero intentamos por nombre directo
            resp = requests.get(
                f"{settings.WAHA_URL}/api/sessions/{settings.WAHA_SESSION}",
                headers=waha_headers(),
                timeout=5,
            )
            if resp.status_code == 200:
                data = resp.json()
                self._sync_account(data)
                return Response(data)

            # Si no existe por nombre, listamos todas las sesiones
            resp_all = requests.get(
                f"{settings.WAHA_URL}/api/sessions",
                headers=waha_headers(),
                timeout=5,
            )
            if resp_all.status_code == 200:
                sessions = resp_all.json()
                for s in (sessions if isinstance(sessions, list) else []):
                    if s.get('name') == settings.WAHA_SESSION:
                        self._sync_account(s)
                        return Response(s)
                return Response({'status': 'STOPPED', 'name': settings.WAHA_SESSION})

            return Response({'status': 'STOPPED', 'name': settings.WAHA_SESSION})
        except Exception as exc:
            return Response({'status': 'ERROR', 'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

    def _sync_account(self, session_data):
        if session_data.get('status') == 'WORKING':
            me = session_data.get('me') or {}
            phone = me.get('id', '') if isinstance(me, dict) else ''
            name = me.get('pushName', '') if isinstance(me, dict) else ''
            if phone:
                WhatsAppAccount.set_active(phone, name)


class SessionStartView(APIView):
    """Inicia o reinicia la sesión WhatsApp."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Detener sesión existente si hay
        try:
            requests.delete(
                f"{settings.WAHA_URL}/api/sessions/{settings.WAHA_SESSION}",
                headers=waha_headers(),
                timeout=5,
            )
        except Exception:
            pass

        try:
            resp = requests.post(
                f"{settings.WAHA_URL}/api/sessions",
                json={'name': settings.WAHA_SESSION, 'start': True},
                headers=waha_headers(),
                timeout=10,
            )
            # 201 = creada, 200 = ya existía, ambas son éxito
            if resp.status_code in (200, 201):
                try:
                    return Response(resp.json())
                except Exception:
                    return Response({'status': 'STARTING', 'name': settings.WAHA_SESSION})
            resp.raise_for_status()
            return Response({'status': 'STARTING', 'name': settings.WAHA_SESSION})
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)


class SessionQRView(APIView):
    """Devuelve el QR de autenticación como imagen PNG — AllowAny porque es una imagen temporal."""
    permission_classes = [AllowAny]

    def get(self, request):
        from django.http import HttpResponse
        try:
            resp = requests.get(
                f"{settings.WAHA_URL}/api/{settings.WAHA_SESSION}/auth/qr",
                headers=waha_headers(),
                timeout=10,
                stream=True,
            )
            resp.raise_for_status()
            content_type = resp.headers.get('content-type', 'image/png')
            return HttpResponse(resp.content, content_type=content_type)
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)


class SessionLogoutView(APIView):
    """Cierra y elimina la sesión WhatsApp."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            resp = requests.delete(
                f"{settings.WAHA_URL}/api/sessions/{settings.WAHA_SESSION}",
                headers=waha_headers(),
                timeout=10,
            )
            if resp.status_code in (200, 404):
                WhatsAppAccount.deactivate()
                return Response({'ok': True})
            resp.raise_for_status()
            return Response({'ok': True})
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
