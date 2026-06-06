from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import ReadOnlyOrAdmin
from .models import Category, Package, Itinerary
from .serializers import (
    CategorySerializer,
    PackageListSerializer,
    PackageDetailSerializer,
    PackageCreateSerializer,
    ItinerarySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías de paquetes"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Se encontraron {queryset.count()} categorías',
            'categorias': serializer.data
        })


class PackageViewSet(viewsets.ModelViewSet):
    """ViewSet para paquetes turísticos"""
    queryset = Package.objects.select_related('destination', 'category').all()
    permission_classes = [ReadOnlyOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'destination', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'destination__name']
    ordering_fields = ['price_adult', 'created_at', 'duration_days']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PackageListSerializer
        elif self.action == 'retrieve':
            return PackageDetailSerializer
        return PackageCreateSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price:
            queryset = queryset.filter(price_adult__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price_adult__lte=max_price)
        
        min_days = self.request.query_params.get('min_days', None)
        if min_days:
            queryset = queryset.filter(duration_days__gte=min_days)

        max_days = self.request.query_params.get('max_days', None)
        if max_days:
            queryset = queryset.filter(duration_days__lte=max_days)

        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'exito': True,
                'mensaje': f'Se encontraron {queryset.count()} paquetes',
                'paquetes': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Se encontraron {queryset.count()} paquetes',
            'paquetes': serializer.data
        })
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'exito': True,
            'mensaje': 'Paquete encontrado',
            'paquete': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Error al crear el paquete',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response({
            'exito': True,
            'mensaje': 'Paquete creado exitosamente',
            'paquete': serializer.data
        }, status=status.HTTP_201_CREATED)


class ItineraryViewSet(viewsets.ModelViewSet):
    """ViewSet para itinerarios de paquetes (CRUD completo para admins)"""
    serializer_class = ItinerarySerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        package_id = self.kwargs.get('package_pk')
        if package_id:
            return Itinerary.objects.filter(package_id=package_id).order_by('day_number')
        return Itinerary.objects.none()

    def perform_create(self, serializer):
        package_id = self.kwargs.get('package_pk')
        serializer.save(package_id=package_id)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response({'exito': True, 'itinerario': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors}, status=400)
        self.perform_create(serializer)
        return Response({'exito': True, 'mensaje': 'Día creado', 'dia': serializer.data}, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors}, status=400)
        self.perform_update(serializer)
        return Response({'exito': True, 'mensaje': 'Día actualizado', 'dia': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'exito': True, 'mensaje': 'Día eliminado'}, status=204)
