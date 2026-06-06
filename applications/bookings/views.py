import stripe
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsOwnerOrAdmin, IsAdminUser
from .emails import send_booking_confirmation, send_payment_confirmation, send_booking_cancellation
from applications.authentication.notifications import (
    notify_booking_created, notify_payment_confirmed, notify_booking_cancelled,
    notify_booking_confirmed, notify_booking_completed,
)
from .models import Booking
from .serializers import (
    BookingListSerializer,
    BookingDetailSerializer,
    BookingCreateSerializer,
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet para reservas"""
    queryset = Booking.objects.select_related(
        'customer', 'package'
    ).prefetch_related(
        'passengers',
        'hotel_bookings',
        'flight_bookings'
    ).all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'package_id', 'status', 'payment_status']
    search_fields = ['booking_number', 'customer__email', 'customer__first_name']
    ordering_fields = ['booking_date', 'travel_date', 'total_amount']
    ordering = ['-booking_date']

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsOwnerOrAdmin()]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookingListSerializer
        elif self.action == 'retrieve':
            return BookingDetailSerializer
        elif self.action == 'create':
            return BookingCreateSerializer
        return BookingDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 'admin':
            pass
        else:
            queryset = queryset.filter(customer=self.request.user)

        travel_date_from = self.request.query_params.get('travel_date_from', None)
        travel_date_to = self.request.query_params.get('travel_date_to', None)
        if travel_date_from:
            queryset = queryset.filter(travel_date__gte=travel_date_from)
        if travel_date_to:
            queryset = queryset.filter(travel_date__lte=travel_date_to)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'exito': True,
                'mensaje': f'Tienes {queryset.count()} reservas',
                'reservas': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Tienes {queryset.count()} reservas',
            'reservas': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Error al crear la reserva',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        booking = serializer.save(customer=request.user)
        # Incrementar cupos usados
        if booking.package_id:
            from django.db.models import F
            from applications.packages.models import Package as PkgModel
            PkgModel.objects.filter(pk=booking.package_id).update(
                booked_count=F('booked_count') + 1
            )
        send_booking_confirmation(booking)
        notify_booking_created(booking)
        return Response({
            'exito': True,
            'mensaje': '¡Tu reserva ha sido confirmada exitosamente!',
            'numero_reserva': booking.booking_number,
            'detalles': BookingDetailSerializer(booking).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_bookings(self, request):
        """GET /api/bookings/my_bookings/"""
        bookings = self.queryset.filter(customer=request.user)
        serializer = BookingListSerializer(bookings, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Tienes {bookings.count()} reservas',
            'reservas': serializer.data
        })

    @action(detail=True, methods=['patch'], permission_classes=[IsOwnerOrAdmin])
    def cancel(self, request, pk=None):
        """PATCH /api/bookings/{id}/cancel/"""
        booking = self.get_object()
        if booking.status == 'cancelled':
            return Response({
                'exito': False,
                'mensaje': 'Esta reserva ya fue cancelada anteriormente'
            }, status=status.HTTP_400_BAD_REQUEST)
        if booking.status == 'completed':
            return Response({
                'exito': False,
                'mensaje': 'No es posible cancelar una reserva que ya fue completada'
            }, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        # Decrementar cupos usados
        if booking.package_id:
            from django.db.models import F
            from applications.packages.models import Package as PkgModel
            PkgModel.objects.filter(pk=booking.package_id, booked_count__gt=0).update(
                booked_count=F('booked_count') - 1
            )
        send_booking_cancellation(booking)
        notify_booking_cancelled(booking)
        return Response({
            'exito': True,
            'mensaje': 'Tu reserva ha sido cancelada exitosamente',
            'numero_reserva': booking.booking_number,
            'detalles': BookingDetailSerializer(booking).data
        })

    def partial_update(self, request, *args, **kwargs):
        booking = self.get_object()
        old_status = booking.status
        response = super().partial_update(request, *args, **kwargs)
        if response.status_code == 200:
            booking.refresh_from_db()
            new_status = booking.status
            if old_status != new_status:
                if new_status == Booking.STATUS_CONFIRMED:
                    notify_booking_confirmed(booking)
                elif new_status == Booking.STATUS_COMPLETED:
                    notify_booking_completed(booking)
                elif new_status == Booking.STATUS_CANCELLED:
                    notify_booking_cancelled(booking)
        return response

    def destroy(self, request, *args, **kwargs):
        """DELETE /api/bookings/{id}/"""
        booking = self.get_object()
        if not (request.user.user_type == 'admin' or booking.customer == request.user):
            return Response({
                'exito': False,
                'mensaje': 'No tienes permiso para eliminar esta reserva.'
            }, status=status.HTTP_403_FORBIDDEN)
        if booking.status == 'completed':
            return Response({
                'exito': False,
                'mensaje': 'No puedes eliminar una reserva que ya fue completada.'
            }, status=status.HTTP_400_BAD_REQUEST)
        booking_number = booking.booking_number
        booking.delete()
        return Response({
            'exito': True,
            'mensaje': f'La reserva {booking_number} ha sido eliminada correctamente.'
        }, status=status.HTTP_204_NO_CONTENT)

    # ─── Stripe payment actions ────────────────────────────────────────────────

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def refund(self, request, pk=None):
        """POST /api/bookings/{id}/refund/  — Admin marca la reserva como reembolsada"""
        booking = self.get_object()

        if booking.payment_status == Booking.PAYMENT_REFUNDED:
            return Response({'exito': False, 'mensaje': 'Esta reserva ya fue reembolsada.'}, status=400)
        if booking.payment_status not in (Booking.PAYMENT_PAID, Booking.PAYMENT_PARTIAL):
            return Response({'exito': False, 'mensaje': 'Solo se pueden reembolsar reservas que tengan un pago registrado.'}, status=400)

        refund_amount = request.data.get('refund_amount')
        reason = request.data.get('reason', '').strip()

        try:
            if refund_amount is not None:
                amount = Decimal(str(refund_amount))
                if amount <= 0 or amount > booking.paid_amount:
                    return Response({'exito': False, 'mensaje': f'El monto debe estar entre $0.01 y {booking.paid_amount}.'}, status=400)
            else:
                amount = booking.paid_amount
        except (InvalidOperation, TypeError):
            return Response({'exito': False, 'mensaje': 'Monto inválido.'}, status=400)

        booking.payment_status = Booking.PAYMENT_REFUNDED
        booking.status = Booking.STATUS_CANCELLED
        notes = f'Reembolso de ${amount} procesado por {request.user.email}.'
        if reason:
            notes += f' Motivo: {reason}'
        if booking.special_requests:
            booking.special_requests = booking.special_requests + '\n' + notes
        else:
            booking.special_requests = notes
        booking.save(update_fields=['payment_status', 'status', 'special_requests', 'updated_at'])

        # Liberar cupo
        if booking.package_id:
            from django.db.models import F
            from applications.packages.models import Package as PkgModel
            PkgModel.objects.filter(pk=booking.package_id, booked_count__gt=0).update(
                booked_count=F('booked_count') - 1
            )

        notify_booking_cancelled(booking)
        return Response({
            'exito': True,
            'mensaje': f'Reembolso de {amount} registrado correctamente.',
            'detalles': BookingDetailSerializer(booking).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrAdmin])
    def create_payment_intent(self, request, pk=None):
        """POST /api/bookings/{id}/create_payment_intent/"""
        booking = self.get_object()

        if booking.payment_status == Booking.PAYMENT_PAID:
            return Response({
                'exito': False,
                'mensaje': 'Esta reserva ya ha sido pagada completamente.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if booking.status == Booking.STATUS_CANCELLED:
            return Response({
                'exito': False,
                'mensaje': 'No se puede pagar una reserva cancelada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount_cents = int(Decimal(str(booking.total_amount)) * 100)
        except (InvalidOperation, TypeError):
            return Response({
                'exito': False,
                'mensaje': 'El monto de la reserva no es válido.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if amount_cents <= 0:
            return Response({
                'exito': False,
                'mensaje': 'El monto a pagar debe ser mayor a cero.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency='usd',
                payment_method_types=['card'],
                metadata={
                    'booking_id': str(booking.id),
                    'booking_number': booking.booking_number,
                    'customer_email': booking.customer.email,
                },
                description=f'Reserva #{booking.booking_number} — {booking.customer.email}',
            )
        except stripe.error.StripeError as e:
            return Response({
                'exito': False,
                'mensaje': f'Error al crear el pago: {e.user_message}'
            }, status=status.HTTP_502_BAD_GATEWAY)

        return Response({
            'exito': True,
            'mensaje': 'Intención de pago creada. Ingresa los datos de tu tarjeta.',
            'client_secret': payment_intent.client_secret,
            'payment_intent_id': payment_intent.id,
            'amount': str(booking.total_amount),
            'currency': 'usd',
        })

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrAdmin])
    def confirm_payment(self, request, pk=None):
        """POST /api/bookings/{id}/confirm_payment/"""
        booking = self.get_object()
        pi_id = request.data.get('payment_intent_id', '').strip()

        if not pi_id:
            return Response({
                'exito': False,
                'mensaje': 'Se requiere el ID de la intención de pago.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_intent = stripe.PaymentIntent.retrieve(pi_id)
        except stripe.error.InvalidRequestError:
            return Response({
                'exito': False,
                'mensaje': 'La intención de pago no existe o es inválida.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({
                'exito': False,
                'mensaje': f'Error al verificar el pago: {e.user_message}'
            }, status=status.HTTP_502_BAD_GATEWAY)

        pi_booking_id = payment_intent.metadata['booking_id'] if payment_intent.metadata else None
        if pi_booking_id != str(booking.id):
            return Response({
                'exito': False,
                'mensaje': 'Esta transacción no corresponde a la reserva indicada.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if payment_intent.status != 'succeeded':
            return Response({
                'exito': False,
                'mensaje': f'El pago no fue completado. Estado: {payment_intent.status}'
            }, status=status.HTTP_400_BAD_REQUEST)

        booking.paid_amount = Decimal(str(payment_intent.amount_received)) / 100
        booking.payment_status = Booking.PAYMENT_PAID
        booking.status = Booking.STATUS_CONFIRMED
        booking.save(update_fields=['paid_amount', 'payment_status', 'status', 'updated_at'])
        send_payment_confirmation(booking)
        notify_payment_confirmed(booking)

        return Response({
            'exito': True,
            'mensaje': '¡Pago realizado con éxito! Tu reserva ha sido confirmada.',
            'numero_reserva': booking.booking_number,
            'detalles': BookingDetailSerializer(booking).data
        })


# ─── Stripe Webhook ────────────────────────────────────────────────────────────

class AdminMetricsView(APIView):
    """
    GET /api/bookings/metrics/
    Métricas para el dashboard de administrador.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        from applications.authentication.models import User
        from applications.reviews.models import Review

        now = timezone.now()
        twelve_months_ago = now - timezone.timedelta(days=365)

        # ── Totales ────────────────────────────────────────────────────────────
        total_bookings = Booking.objects.count()
        total_revenue = (
            Booking.objects.filter(payment_status='paid')
            .aggregate(total=Sum('paid_amount'))['total'] or Decimal('0')
        )
        total_users = User.objects.filter(user_type='customer').count()
        new_users_this_month = User.objects.filter(
            date_joined__year=now.year,
            date_joined__month=now.month,
            user_type='customer',
        ).count()
        pending_reviews = Review.objects.filter(is_approved=False).count()
        avg_rating = Review.objects.aggregate(avg=Avg('overall_rating'))['avg'] or 0

        # ── Reservas por estado ────────────────────────────────────────────────
        status_counts = {
            row['status']: row['count']
            for row in Booking.objects.values('status').annotate(count=Count('id'))
        }

        # ── Ingresos por mes (últimos 12 meses) ────────────────────────────────
        monthly_revenue = list(
            Booking.objects.filter(
                payment_status='paid',
                booking_date__gte=twelve_months_ago,
            )
            .annotate(month=TruncMonth('booking_date'))
            .values('month')
            .annotate(revenue=Sum('paid_amount'), bookings=Count('id'))
            .order_by('month')
            .values('month', 'revenue', 'bookings')
        )
        monthly_revenue_data = [
            {
                'month': row['month'].strftime('%Y-%m'),
                'revenue': float(row['revenue'] or 0),
                'bookings': row['bookings'],
            }
            for row in monthly_revenue
        ]

        # ── Top 5 paquetes más reservados ──────────────────────────────────────
        top_packages = list(
            Booking.objects.exclude(status='cancelled')
            .values('package__name')
            .annotate(count=Count('id'), revenue=Sum('paid_amount'))
            .order_by('-count')[:5]
        )
        top_packages_data = [
            {
                'name': row['package__name'] or 'Sin nombre',
                'bookings': row['count'],
                'revenue': float(row['revenue'] or 0),
            }
            for row in top_packages
        ]

        return Response({
            'exito': True,
            'totales': {
                'reservas': total_bookings,
                'ingresos': float(total_revenue),
                'usuarios': total_users,
                'nuevos_este_mes': new_users_this_month,
                'reseñas_pendientes': pending_reviews,
                'calificacion_promedio': round(float(avg_rating), 1),
            },
            'estados': {
                'pending': status_counts.get('pending', 0),
                'confirmed': status_counts.get('confirmed', 0),
                'cancelled': status_counts.get('cancelled', 0),
                'completed': status_counts.get('completed', 0),
            },
            'ingresos_mensuales': monthly_revenue_data,
            'top_paquetes': top_packages_data,
        })


class StripeWebhookView(APIView):
    """
    POST /api/payments/webhook/
    Backup: actualiza la reserva cuando Stripe confirma el pago vía webhook.
    No usa JWT — la seguridad viene de la firma del webhook.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event['type'] == 'payment_intent.succeeded':
            pi = event['data']['object']
            booking_id = (pi.get('metadata') or {}).get('booking_id')
            if booking_id:
                try:
                    booking = Booking.objects.get(id=booking_id)
                    if booking.payment_status != Booking.PAYMENT_PAID:
                        booking.paid_amount = Decimal(pi.get('amount_received', 0)) / 100
                        booking.payment_status = Booking.PAYMENT_PAID
                        booking.status = Booking.STATUS_CONFIRMED
                        booking.save(update_fields=[
                            'paid_amount', 'payment_status', 'status', 'updated_at'
                        ])
                except Booking.DoesNotExist:
                    pass

        return HttpResponse(status=200)
