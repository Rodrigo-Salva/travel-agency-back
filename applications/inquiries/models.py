from django.db import models


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nueva'),
        ('in_progress', 'En Progreso'),
        ('responded', 'Respondida'),
        ('closed', 'Cerrada'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    email = models.EmailField(max_length=254, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    subject = models.CharField(max_length=200, verbose_name='Asunto')
    message = models.TextField(verbose_name='Mensaje')
    
    package = models.ForeignKey(
        'packages.Package',
        on_delete=models.SET_NULL,
        related_name='inquiries',
        verbose_name='Paquete',
        null=True,
        blank=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Estado'
    )
    
    admin_response = models.TextField(
        verbose_name='Respuesta del Administrador',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        db_table = 'consultas'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email']),
            models.Index(fields=['package']),
        ]
    
    def __str__(self):
        return f"{self.subject} - {self.name} ({self.get_status_display()})"