from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Package, Itinerary
from .serializers import CategorySerializer, PackageListSerializer, PackageDetailSerializer, ItinerarySerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías de paquetes"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['name']

class PackageViewSet(viewsets.ModelViewSet):
    """ViewSet para paquetes turísticos"""
    queryset = Package.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'destination__name']
    ordering_fields = ['name', 'price_adult', 'duration_days', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Usar serializer diferente según la acción"""
        if self.action == 'list':
            return PackageListSerializer
        return PackageDetailSerializer
    
    def get_queryset(self):
        """Filtrar solo paquetes activos por defecto"""
        queryset = Package.objects.filter(is_active=True)
        
        # Si es admin, mostrar todos los paquetes
        if self.request.user.is_staff:
            queryset = Package.objects.all()
            
        return queryset

class ItineraryViewSet(viewsets.ModelViewSet):
    """ViewSet para itinerarios de paquetes"""
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['package', 'day_number']
    ordering_fields = ['day_number']
    ordering = ['day_number']