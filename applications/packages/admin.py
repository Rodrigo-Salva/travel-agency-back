from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Package, Itinerary,Wishlist


class ItineraryInline(admin.TabularInline):
    """Inline para gestionar itinerarios dentro del admin de paquetes"""
    model = Itinerary
    extra = 1
    fields = ['day_number', 'title', 'description', 'activities', 'meals_included']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin para categorías"""
    list_display = ['name', 'icon', 'packages_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def packages_count(self, obj):
        """Mostrar número de paquetes en la categoría"""
        return obj.packages.count()
    packages_count.short_description = 'Número de Paquetes'


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    """Admin para paquetes turísticos"""
    list_display = [
        'name', 'category', 'destination', 'price_adult', 
        'duration_days', 'is_featured', 'available_from', 'created_at'
    ]
    list_filter = [
        'category', 'destination', 'is_featured', 'available_from', 
        'available_until', 'created_at'
    ]
    search_fields = [
        'name', 'description', 'short_description', 
        'destination__name', 'destination__city', 'destination__country'
    ]
    readonly_fields = ['slug', 'created_at', 'updated_at']
    inlines = [ItineraryInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'category', 'destination', 'description', 'short_description')
        }),
        ('Detalles del Paquete', {
            'fields': ('duration_days', 'duration_nights', 'price_adult', 'price_child', 'max_people', 'min_people')
        }),
        ('Incluye y Características', {
            'fields': ('includes', 'image', 'is_featured')
        }),
        ('Disponibilidad', {
            'fields': ('available_from', 'available_until')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    """Admin para itinerarios"""
    list_display = ['package', 'day_number', 'title', 'created_at']
    list_filter = ['package', 'day_number', 'created_at']
    search_fields = ['package__name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Optimizar consultas"""
        return super().get_queryset(request).select_related('package')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'package',
        'added_at',
    ]
    
    list_filter = [
        'added_at',
    ]
    
    search_fields = [
        'user__username',
        'user__email',
        'package__name',
    ]
    
    readonly_fields = ['added_at']
    
    fieldsets = (
        ('Información', {
            'fields': ('user', 'package')
        }),
        ('Información Adicional', {
            'fields': ('added_at',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'package')