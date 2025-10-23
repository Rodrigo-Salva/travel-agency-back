from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    """Modelo para destinos turísticos"""
    name = models.CharField(max_length=200, verbose_name="Nombre del destino")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    country = models.CharField(max_length=100, verbose_name="País")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    description = models.TextField(verbose_name="Descripción")
    short_description = models.CharField(max_length=300, verbose_name="Descripción corta")
    image = models.ImageField(upload_to='destinations/', blank=True, null=True, verbose_name="Imagen principal")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        db_table = "destinos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
