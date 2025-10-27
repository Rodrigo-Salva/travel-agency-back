from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from core.permissions import ReadOnlyOrAdmin
from .models import Category, Package, Wishlist
from .serializers import (
    CategorySerializer,
    PackageListSerializer,
    PackageDetailSerializer,
    PackageCreateSerializer,
    WishlistSerializer
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


class WishlistViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar la lista de deseos de los usuarios"""
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retornar solo los items de wishlist del usuario actual"""
        return Wishlist.objects.filter(user=self.request.user).select_related('package')
    
    def list(self, request, *args, **kwargs):
        """Listar todos los paquetes en la wishlist del usuario"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Se encontraron {queryset.count()} paquetes en tu lista de deseos',
            'wishlist': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        """Agregar un paquete a la wishlist"""
        # Aceptar tanto 'package' como 'package_id'
        package_id = request.data.get('package_id') or request.data.get('package')
        
        if not package_id:
            return Response({
                'exito': False,
                'mensaje': 'El ID del paquete es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar si ya existe en la wishlist
        if Wishlist.objects.filter(user=request.user, package_id=package_id).exists():
            return Response({
                'exito': False,
                'mensaje': 'Este paquete ya está en tu lista de deseos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Normalizar los datos para el serializer
        data = {'package_id': package_id}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'exito': True,
                'mensaje': 'Paquete agregado a la lista de deseos',
                'wishlist_item': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'exito': False,
            'mensaje': 'Error al agregar a la lista de deseos',
            'errores': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """Eliminar un paquete de la wishlist"""
        instance = self.get_object()
        instance.delete()
        return Response({
            'exito': True,
            'mensaje': 'Paquete eliminado de la lista de deseos'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        """Obtener el conteo de items en la wishlist"""
        count = self.get_queryset().count()
        return Response({
            'exito': True,
            'count': count
        })
    
    @action(detail=False, methods=['post'], url_path='toggle/(?P<package_id>[^/.]+)')
    def toggle(self, request, package_id=None):
        """Toggle: agregar o quitar un paquete de la wishlist"""
        package = get_object_or_404(Package, id=package_id)
        
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            package=package
        ).first()
        
        if wishlist_item:
            # Si existe, eliminarlo
            wishlist_item.delete()
            return Response({
                'exito': True,
                'mensaje': 'Paquete eliminado de la lista de deseos',
                'in_wishlist': False
            }, status=status.HTTP_200_OK)
        else:
            # Si no existe, agregarlo
            wishlist_item = Wishlist.objects.create(
                user=request.user,
                package=package
            )
            serializer = self.get_serializer(wishlist_item)
            return Response({
                'exito': True,
                'mensaje': 'Paquete agregado a la lista de deseos',
                'in_wishlist': True,
                'wishlist_item': serializer.data
            }, status=status.HTTP_201_CREATED)