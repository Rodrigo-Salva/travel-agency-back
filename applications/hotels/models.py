from django.db import models

# Create your models here.

class Hotel(models.Model):
    """Modelo para hoteles"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    address = models.CharField(max_length=300, verbose_name="Dirección")
    rating = models.IntegerField(default=0, verbose_name="Calificación")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por noche")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.rating} estrellas"