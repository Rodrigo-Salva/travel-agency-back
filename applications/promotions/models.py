from django.db import models

# Create your models here.

class Promotion(models.Model):
    """Modelo para promociones"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Porcentaje de descuento")
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de fin")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.discount_percentage}% descuento"