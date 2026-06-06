from django.db import models
from applications.packages.models import Package


class Inquiry(models.Model):
    """
    Consultas y cotizaciones de clientes
    """

    TYPE_INQUIRY = 'inquiry'
    TYPE_QUOTE = 'quote'
    TYPE_CHOICES = (
        (TYPE_INQUIRY, 'Consulta general'),
        (TYPE_QUOTE, 'Solicitud de cotización'),
    )

    STATUS_CHOICES = (
        ('new', 'Nueva'),
        ('in_progress', 'En progreso'),
        ('responded', 'Respondida'),
        ('closed', 'Cerrada'),
    )
    
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre'
    )
    
    email = models.EmailField(
        verbose_name='Email'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    subject = models.CharField(
        max_length=200,
        verbose_name='Asunto'
    )
    
    message = models.TextField(
        verbose_name='Mensaje'
    )
    
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='inquiries',
        verbose_name='Paquete relacionado'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Estado'
    )
    
    inquiry_type = models.CharField(
        max_length=16,
        choices=TYPE_CHOICES,
        default=TYPE_INQUIRY,
        verbose_name='Tipo'
    )

    # Campos extra para cotizaciones
    destination_text = models.CharField(max_length=200, blank=True, null=True, verbose_name='Destino deseado')
    departure_date   = models.DateField(blank=True, null=True, verbose_name='Fecha de salida aproximada')
    return_date      = models.DateField(blank=True, null=True, verbose_name='Fecha de regreso aproximada')
    num_adults       = models.PositiveIntegerField(default=1, blank=True, null=True, verbose_name='Adultos')
    num_children     = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Niños')
    budget           = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Presupuesto (USD)')
    interests        = models.TextField(blank=True, null=True, verbose_name='Intereses / actividades deseadas')

    admin_response = models.TextField(
        blank=True,
        null=True,
        verbose_name='Respuesta del administrador'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        db_table = 'consultas'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"