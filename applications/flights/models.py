from django.db import models

# Modelo creado para que los FK funcionen correctamente
class Flight(models.Model):
	flight_number = models.CharField(max_length=64)
	departure = models.CharField(max_length=128, blank=True, null=True)
	arrival = models.CharField(max_length=128, blank=True, null=True)

	def __str__(self):
		return self.flight_number
