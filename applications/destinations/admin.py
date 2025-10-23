from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    """Admin para destinos turísticos"""
    list_display = ['name', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['country', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'country', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'country', 'city', 'description', 'short_description')
        }),
        ('Imagen y Estado', {
            'fields': ('image', 'is_active')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
