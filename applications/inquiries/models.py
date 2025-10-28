from django.db import models

# Create your models here.

class Inquiry(models.Model):
    """Modelo para consultas"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    is_responded = models.BooleanField(default=False, verbose_name="Respondida")
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Consulta de {self.name} - {self.subject}"