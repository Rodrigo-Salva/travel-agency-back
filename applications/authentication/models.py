from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """
    Modelo de Usuario personalizado para la agencia de turismo
    Extiende el usuario por defecto de Django
    """
    
    # Choices para tipo de usuario
    USER_TYPES = (
        ('admin', 'Administrador'),
        ('customer', 'Cliente'),
    )
    
    # Campos adicionales
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='customer',
        verbose_name='Tipo de usuario'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Ciudad'
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='País'
    )
    
    passport_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número de Pasaporte'
    )
    
    nationality = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nacionalidad'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"


class Notification(models.Model):
    TYPE_BOOKING   = 'booking'
    TYPE_PAYMENT   = 'payment'
    TYPE_REVIEW    = 'review'
    TYPE_PROMO     = 'promo'
    TYPE_SYSTEM    = 'system'

    TYPE_CHOICES = [
        (TYPE_BOOKING, 'Reserva'),
        (TYPE_PAYMENT, 'Pago'),
        (TYPE_REVIEW,  'Reseña'),
        (TYPE_PROMO,   'Promoción'),
        (TYPE_SYSTEM,  'Sistema'),
    ]

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type       = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_SYSTEM)
    title      = models.CharField(max_length=200)
    message    = models.TextField()
    is_read    = models.BooleanField(default=False)
    link       = models.CharField(max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.title}"
