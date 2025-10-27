from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    country = models.CharField(max_length=100, verbose_name='País')
    continent = models.CharField(max_length=50, verbose_name='Continente')
    description = models.TextField(verbose_name='Descripción')
    short_description = models.CharField(max_length=300, verbose_name='Descripción corta')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitud')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitud')
    image = models.ImageField(upload_to='destinations/', blank=True, null=True, verbose_name='Imagen')
    is_popular = models.BooleanField(default=False, verbose_name='Es popular')
    best_season = models.CharField(max_length=100, verbose_name='Mejor temporada')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'destinos'
        ordering = ['-created_at']
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'

    def __str__(self):
        return f"{self.name} ({self.country})"

