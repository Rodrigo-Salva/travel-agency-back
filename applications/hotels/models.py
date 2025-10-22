from django.db import models

# Modelo creado para que los FK funcionen correctamente
class Hotel(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.name
