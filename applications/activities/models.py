from django.db import models

# Create your models here.

class Activity(models.Model):
    """Modelo para actividades"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    category = models.CharField(max_length=100, verbose_name="Categoría")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    duration_hours = models.PositiveIntegerField(verbose_name="Duración en horas")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.category}"