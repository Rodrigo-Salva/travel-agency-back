from django.db import models

# Create your models here.

class Flight(models.Model):
    """Modelo para vuelos"""
    flight_number = models.CharField(max_length=20, verbose_name="Número de vuelo")
    origin = models.CharField(max_length=100, verbose_name="Origen")
    destination = models.CharField(max_length=100, verbose_name="Destino")
    departure_time = models.DateTimeField(verbose_name="Hora de salida")
    arrival_time = models.DateTimeField(verbose_name="Hora de llegada")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Vuelo"
        verbose_name_plural = "Vuelos"
        ordering = ['departure_time']
    
    def __str__(self):
        return f"{self.flight_number} - {self.origin} a {self.destination}"