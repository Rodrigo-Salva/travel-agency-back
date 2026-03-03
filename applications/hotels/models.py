from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nombre')
    destination = models.ForeignKey(
        'destinations.Destination', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='hotels',
        verbose_name='Destino'
    )
    address = models.CharField(max_length=255, verbose_name='Dirección')
    star_rating = models.PositiveIntegerField(default=3, verbose_name='Calificación de estrellas')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción')
    amenities = models.TextField(blank=True, null=True, verbose_name='Amenidades')
    check_in_time = models.TimeField(null=True, blank=True, verbose_name='Hora de check-in')
    check_out_time = models.TimeField(null=True, blank=True, verbose_name='Hora de check-out')
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name='Teléfono')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='Correo electrónico')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio por noche')
    total_rooms = models.PositiveIntegerField(verbose_name='Total de habitaciones')
    image = models.ImageField(upload_to='hotels/', blank=True, null=True, verbose_name='Imagen')
    is_active = models.BooleanField(default=True, verbose_name='Está activo')

    class Meta:
        db_table = 'hoteles'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'

    def __str__(self):
        return self.name