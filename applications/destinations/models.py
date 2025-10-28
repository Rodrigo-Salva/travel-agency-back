from django.db import models

# Create your models here.

class Destination(models.Model):
    """Modelo para destinos turísticos"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    country = models.CharField(max_length=100, verbose_name="País")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    image = models.ImageField(upload_to='destinations/', null=True, blank=True, verbose_name="Imagen")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"