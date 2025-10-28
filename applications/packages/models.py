from django.db import models
from django.utils.text import slugify
from applications.destinations.models import Destination

# Create your models here.

class Category(models.Model):
    """Modelo para categorías de paquetes"""
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icono")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = 'categorias_paquetes'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Package(models.Model):
    """Modelo para paquetes turísticos"""
    INCLUDE_CHOICES = [
        ('flight', 'Vuelo'),
        ('hotel', 'Hotel'),
        ('meals', 'Comidas'),
        ('transport', 'Transporte'),
        ('guide', 'Guía'),
        ('insurance', 'Seguro'),
        ('activities', 'Actividades'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoría", null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name="Destino", null=True, blank=True)
    description = models.TextField(verbose_name="Descripción", blank=True)
    duration_days = models.PositiveIntegerField(verbose_name="Duración en días", default=1)
    duration_nights = models.PositiveIntegerField(verbose_name="Duración en noches", default=0)
    price_adult = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio adulto", default=0)
    price_child = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio niño", default=0)
    max_people = models.PositiveIntegerField(default=10, verbose_name="Máximo de personas")
    includes = models.JSONField(default=list, verbose_name="Incluye")
    image = models.ImageField(upload_to='packages/', null=True, blank=True, verbose_name="Imagen")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    available_from = models.DateField(verbose_name="Disponible desde", default='2024-01-01')
    available_until = models.DateField(verbose_name="Disponible hasta", default='2024-12-31')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        db_table = 'paquetes_turisticos'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class Itinerary(models.Model):
    """Modelo para itinerarios de paquetes"""
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='itineraries', verbose_name="Paquete")
    day_number = models.PositiveIntegerField(verbose_name="Día número")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    activities = models.JSONField(default=list, verbose_name="Actividades")
    meals_included = models.JSONField(default=list, verbose_name="Comidas incluidas")
    
    class Meta:
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerarios"
        db_table = 'itinerarios_paquete'
        ordering = ['day_number']
        unique_together = ['package', 'day_number']
    
    def __str__(self):
        return f"Día {self.day_number} - {self.title}"
