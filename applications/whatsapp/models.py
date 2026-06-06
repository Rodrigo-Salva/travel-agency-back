from django.db import models
from django.conf import settings


class WhatsAppAccount(models.Model):
    """Número de WhatsApp que está conectado actualmente como agente."""
    phone = models.CharField(max_length=50, unique=True, verbose_name='Teléfono')
    push_name = models.CharField(max_length=200, blank=True, verbose_name='Nombre')
    is_active = models.BooleanField(default=True)
    connected_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'whatsapp_accounts'
        verbose_name = 'Cuenta WhatsApp'

    def __str__(self):
        return self.push_name or self.phone

    @classmethod
    def get_active_phone(cls):
        acc = cls.objects.filter(is_active=True).first()
        return acc.phone if acc else ''

    @classmethod
    def set_active(cls, phone, push_name=''):
        cls.objects.all().update(is_active=False)
        obj, _ = cls.objects.update_or_create(
            phone=phone,
            defaults={'push_name': push_name, 'is_active': True},
        )
        return obj

    @classmethod
    def deactivate(cls):
        cls.objects.all().update(is_active=False)


class WhatsAppContact(models.Model):
    phone = models.CharField(max_length=50, unique=True, verbose_name='Teléfono')
    name = models.CharField(max_length=200, blank=True, verbose_name='Nombre')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whatsapp_contacts'
        verbose_name = 'Contacto WhatsApp'
        verbose_name_plural = 'Contactos WhatsApp'
        ordering = ['name']

    def __str__(self):
        return self.name or self.phone


class WhatsAppConversation(models.Model):
    contact = models.OneToOneField(
        WhatsAppContact,
        on_delete=models.CASCADE,
        related_name='conversation',
    )
    owner_phone = models.CharField(max_length=50, blank=True, default='', db_index=True,
                                   verbose_name='Cuenta propietaria')
    last_message_at = models.DateTimeField(null=True, blank=True)
    unread_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'whatsapp_conversations'
        verbose_name = 'Conversación WhatsApp'
        verbose_name_plural = 'Conversaciones WhatsApp'
        ordering = ['-last_message_at']

    def __str__(self):
        return f"Chat con {self.contact}"


class WhatsAppMessage(models.Model):
    DIRECTION_INCOMING = 'incoming'
    DIRECTION_OUTGOING = 'outgoing'
    DIRECTION_CHOICES = [
        (DIRECTION_INCOMING, 'Entrante'),
        (DIRECTION_OUTGOING, 'Saliente'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_QUEUED = 'queued'
    STATUS_SENT = 'sent'
    STATUS_DELIVERED = 'delivered'
    STATUS_READ = 'read'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_QUEUED, 'En cola'),
        (STATUS_SENT, 'Enviado'),
        (STATUS_DELIVERED, 'Entregado'),
        (STATUS_READ, 'Leído'),
        (STATUS_FAILED, 'Fallido'),
        (STATUS_CANCELLED, 'Cancelado'),
    ]

    conversation = models.ForeignKey(
        WhatsAppConversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    content = models.TextField(verbose_name='Contenido')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING)
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name='Programado para')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Enviado a las')
    waha_message_id = models.CharField(max_length=100, null=True, blank=True)
    job_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whatsapp_messages'
        verbose_name = 'Mensaje WhatsApp'
        verbose_name_plural = 'Mensajes WhatsApp'
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.direction}] {self.content[:50]}"


class WhatsAppCampaign(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_RUNNING = 'running'
    STATUS_PAUSED = 'paused'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Borrador'),
        (STATUS_RUNNING, 'En ejecución'),
        (STATUS_PAUSED, 'Pausada'),
        (STATUS_COMPLETED, 'Completada'),
        (STATUS_FAILED, 'Fallida'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nombre')
    message_template = models.TextField(verbose_name='Mensaje')
    contacts = models.ManyToManyField(
        WhatsAppContact,
        related_name='campaigns',
        blank=True,
    )
    delay_between_ms = models.PositiveIntegerField(
        default=5000,
        verbose_name='Delay entre mensajes (ms)',
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='whatsapp_campaigns',
    )
    job_id = models.CharField(max_length=100, null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de envío')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whatsapp_campaigns'
        verbose_name = 'Campaña WhatsApp'
        verbose_name_plural = 'Campañas WhatsApp'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
