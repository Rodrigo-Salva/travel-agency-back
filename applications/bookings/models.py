from django.db import models
from django.contrib.auth.models import User
from applications.packages.models import Package

# Create your models here.

class Booking(models.Model):
    """Modelo para reservas"""
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('cancelled', 'Cancelada'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name="Paquete")
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de reserva")
    travel_date = models.DateField(verbose_name="Fecha de viaje")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reserva {self.id} - {self.user.username} - {self.package.name}"
