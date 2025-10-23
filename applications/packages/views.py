from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Package, Itinerary
from .serializers import CategorySerializer, PackageListSerializer, PackageDetailSerializer, ItinerarySerializer
from applications.destinations.models import Destination


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet para categorías de paquetes"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def packages(self, request, pk=None):
        """Obtener paquetes de una categoría específica"""
        category = self.get_object()
        packages = Package.objects.filter(category=category)
        
        # Aplicar filtros si existen
        if request.query_params.get('featured'):
            packages = packages.filter(is_featured=True)
        
        serializer = PackageListSerializer(packages, many=True, context={'request': request})
        return Response(serializer.data)


class PackageViewSet(viewsets.ModelViewSet):
    """ViewSet para paquetes turísticos"""
    queryset = Package.objects.select_related('category', 'destination').prefetch_related('itineraries')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'short_description', 'destination__name', 'destination__city']
    ordering_fields = ['name', 'price_adult', 'duration_days', 'created_at']
    ordering = ['-created_at']
    filterset_fields = ['category', 'destination', 'is_featured']

    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'list':
            return PackageListSerializer
        elif self.action == 'retrieve':
            return PackageDetailSerializer
        return PackageListSerializer

    def get_queryset(self):
        """Filtrar paquetes según parámetros"""
        queryset = super().get_queryset()
        
        # Filtro por precio mínimo
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(price_adult__gte=min_price)
        
        # Filtro por precio máximo
        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.filter(price_adult__lte=max_price)
        
        # Filtro por duración mínima
        min_duration = self.request.query_params.get('min_duration')
        if min_duration:
            queryset = queryset.filter(duration_days__gte=min_duration)
        
        # Filtro por duración máxima
        max_duration = self.request.query_params.get('max_duration')
        if max_duration:
            queryset = queryset.filter(duration_days__lte=max_duration)
        
        # Filtro por destino (búsqueda por nombre de ciudad o país)
        destination_search = self.request.query_params.get('destination')
        if destination_search:
            queryset = queryset.filter(
                Q(destination__name__icontains=destination_search) |
                Q(destination__city__icontains=destination_search) |
                Q(destination__country__icontains=destination_search)
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Obtener paquetes destacados"""
        featured_packages = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_packages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Obtener paquetes por categoría"""
        category_id = request.query_params.get('category_id')
        if not category_id:
            return Response({'error': 'category_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        packages = self.get_queryset().filter(category_id=category_id)
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_destination(self, request):
        """Obtener paquetes por destino"""
        destination_id = request.query_params.get('destination_id')
        if not destination_id:
            return Response({'error': 'destination_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        packages = self.get_queryset().filter(destination_id=destination_id)
        serializer = self.get_serializer(packages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def itineraries(self, request, pk=None):
        """Obtener itinerarios de un paquete específico"""
        package = self.get_object()
        itineraries = package.itineraries.all()
        serializer = ItinerarySerializer(itineraries, many=True)
        return Response(serializer.data)
