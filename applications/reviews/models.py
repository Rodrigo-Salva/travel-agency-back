from django.db import models
from django.contrib.auth.models import User
from applications.packages.models import Package
from applications.hotels.models import Hotel

# Create your models here.

class Review(models.Model):
    """Modelo para reseñas"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Paquete")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Hotel")
    rating = models.IntegerField(verbose_name="Calificación")
    comment = models.TextField(verbose_name="Comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reseña de {self.user.username} - {self.rating} estrellas"
