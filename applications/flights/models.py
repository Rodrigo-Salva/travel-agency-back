# applications/flights/models.py
from django.db import models
from django.utils import timezone 

class Flight(models.Model):
    airline_name = models.CharField(max_length=100, verbose_name='Aerolínea')
    airline_code = models.CharField(max_length=10, verbose_name='Código de aerolínea')
    flight_number = models.CharField(max_length=20, verbose_name='Número de vuelo')
    origin_city = models.CharField(max_length=100, verbose_name='Ciudad de origen')
    destination_city = models.CharField(max_length=100, verbose_name='Ciudad de destino')
    origin_airport = models.CharField(max_length=100, verbose_name='Aeropuerto de origen')
    destination_airport = models.CharField(max_length=100, verbose_name='Aeropuerto de destino')
    departure_time = models.DateTimeField(verbose_name='Hora de salida')
    arrival_time = models.DateTimeField(verbose_name='Hora de llegada')
    flight_class = models.CharField(max_length=50, verbose_name='Clase de vuelo')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    available_seats = models.PositiveIntegerField(verbose_name='Asientos disponibles')
    baggage_allowance = models.CharField(max_length=100, blank=True, null=True, verbose_name='Equipaje permitido')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'vuelos'
        verbose_name = 'Vuelo'
        verbose_name_plural = 'Vuelos'

    def __str__(self):
        return f"{self.airline_name} {self.flight_number} ({self.origin_city} a {self.destination_city})"