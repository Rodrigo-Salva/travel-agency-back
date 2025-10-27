from django.db import models

class Destination(models.Model):
    name = models.CharField("Nombre del destino", max_length=200)
    country = models.CharField("País", max_length=100)
    continent = models.CharField("Continente", max_length=50)
    description = models.TextField("Descripción")
    short_description = models.CharField("Descripción corta", max_length=300)
    latitude = models.DecimalField("Latitud", max_digits=9, decimal_places=6)
    longitude = models.DecimalField("Longitud", max_digits=9, decimal_places=6)
    image = models.ImageField("Imagen", upload_to='destinations/', blank=True, null=True)
    is_popular = models.BooleanField("Es popular", default=False)
    best_season = models.CharField("Mejor temporada", max_length=100)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        db_table = 'destinos'  
        ordering = ['-created_at']
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"

    def __str__(self):
        return f"{self.name} ({self.country})"
