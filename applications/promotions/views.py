from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from applications.promotions.models import Coupon, Wishlist
from applications.promotions.serializers import (
    CouponSerializer,
    WishlistSerializer,
    CouponValidateSerializer
)


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Hay {queryset.count()} cupones disponibles',
            'cupones': serializer.data
        })
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def validate_coupon(self, request):
        serializer = CouponValidateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'valid': False, 'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        coupon = serializer.validated_data['coupon']
        purchase_amount = serializer.validated_data['purchase_amount']
        discount = coupon.calculate_discount(purchase_amount)
        
        return Response({
            'valid': True,
            'coupon': {
                'code': coupon.code,
                'description': coupon.description,
                'discount_type': coupon.discount_type,
                'discount_value': str(coupon.discount_value),
                'discount_display': coupon.get_discount_display(),
            },
            'discount_amount': str(discount),
            'final_amount': str(purchase_amount - discount)
        })


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.select_related('package')
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Wishlist.objects.all()
        return Wishlist.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Tienes {queryset.count()} paquetes en favoritos',
            'favoritos': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        package_id = request.data.get('package')
        if Wishlist.objects.filter(user=request.user, package_id=package_id).exists():
            return Response({
                'exito': False,
                'mensaje': 'Este paquete ya está en tus favoritos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Error al agregar a favoritos',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        
        return Response({
            'exito': True,
            'mensaje': '¡Paquete agregado a tus favoritos!',
            'favorito': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'exito': True,
            'mensaje': 'Paquete eliminado de tus favoritos'
        }, status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)