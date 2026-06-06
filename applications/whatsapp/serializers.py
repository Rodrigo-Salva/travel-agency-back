from rest_framework import serializers
from .models import WhatsAppContact, WhatsAppConversation, WhatsAppMessage, WhatsAppCampaign


class WhatsAppContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppContact
        fields = ['id', 'phone', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class WhatsAppMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppMessage
        fields = [
            'id', 'conversation', 'direction', 'content', 'status',
            'scheduled_at', 'sent_at', 'waha_message_id', 'job_id', 'created_at',
        ]
        read_only_fields = ['id', 'direction', 'status', 'sent_at', 'waha_message_id', 'job_id', 'created_at']


class WhatsAppConversationSerializer(serializers.ModelSerializer):
    contact = WhatsAppContactSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = WhatsAppConversation
        fields = ['id', 'contact', 'last_message_at', 'unread_count', 'last_message']

    def get_last_message(self, obj):
        msg = obj.messages.last()
        if msg:
            return {'content': msg.content, 'direction': msg.direction, 'status': msg.status}
        return None


class SendMessageSerializer(serializers.Serializer):
    chat_id = serializers.CharField(help_text='Número en formato 51999999999@c.us')
    content = serializers.CharField()
    delay_ms = serializers.IntegerField(default=0, min_value=0, help_text='Delay en milisegundos')
    priority = serializers.IntegerField(default=5, min_value=1, max_value=10)


class WhatsAppCampaignSerializer(serializers.ModelSerializer):
    contact_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=WhatsAppContact.objects.all(),
        source='contacts',
        write_only=True,
        required=False,
    )
    contacts = WhatsAppContactSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = WhatsAppCampaign
        fields = [
            'id', 'name', 'message_template', 'contacts', 'contact_ids',
            'delay_between_ms', 'status', 'created_by', 'job_id', 'scheduled_at', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_by', 'job_id', 'created_at']
