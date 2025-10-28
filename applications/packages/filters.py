import django_filters
from .models import Package

class PackageFilter(django_filters.FilterSet):
    """Filtros para paquetes"""
    
    # Filtros básicos
    category = django_filters.NumberFilter(field_name='category__id')
    destination = django_filters.NumberFilter(field_name='destination__id')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    
    # Filtros de precio
    price_min = django_filters.NumberFilter(field_name='price_adult', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price_adult', lookup_expr='lte')
    
    # Filtros de duración
    duration_min = django_filters.NumberFilter(field_name='duration_days', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration_days', lookup_expr='lte')
    
    # Filtro de capacidad
    max_people = django_filters.NumberFilter(field_name='max_people', lookup_expr='gte')
    
    # Filtro de disponibilidad
    available_from = django_filters.DateFilter(field_name='available_from', lookup_expr='lte')
    available_until = django_filters.DateFilter(field_name='available_until', lookup_expr='gte')
    
    class Meta:
        model = Package
        fields = [
            'category', 'destination', 'is_featured',
            'price_min', 'price_max', 'duration_min', 'duration_max',
            'max_people', 'available_from', 'available_until'
        ]
