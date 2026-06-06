from decimal import Decimal
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Coupon, Wishlist
from .serializers import CouponSerializer, WishlistSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """ViewSet para cupones — CRUD completo para admins, solo lectura para el resto"""
    serializer_class = CouponSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated and getattr(self.request.user, 'user_type', '') == 'admin':
            return Coupon.objects.all().order_by('-created_at')
        return Coupon.objects.filter(is_active=True).order_by('-created_at')

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'validate'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def _is_admin(self):
        return self.request.user and self.request.user.is_authenticated and getattr(self.request.user, 'user_type', '') == 'admin'

    def create(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({'exito': False, 'mensaje': 'Acceso denegado'}, status=403)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors}, status=400)
        serializer.save()
        return Response({'exito': True, 'mensaje': 'Cupón creado', 'cupon': serializer.data}, status=201)

    def update(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({'exito': False, 'mensaje': 'Acceso denegado'}, status=403)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors}, status=400)
        self.perform_update(serializer)
        return Response({'exito': True, 'mensaje': 'Cupón actualizado', 'cupon': serializer.data})

    def destroy(self, request, *args, **kwargs):
        if not self._is_admin():
            return Response({'exito': False, 'mensaje': 'Acceso denegado'}, status=403)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'exito': True, 'mensaje': 'Cupón eliminado'}, status=204)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Hay {queryset.count()} cupones',
            'cupones': serializer.data
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def validate(self, request):
        code = request.data.get('code', '').strip().upper()
        amount = request.data.get('amount', 0)

        if not code:
            return Response({'exito': False, 'mensaje': 'Ingresa un código de cupón'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
        except Coupon.DoesNotExist:
            return Response({'exito': False, 'mensaje': 'Cupón no válido o inactivo'}, status=status.HTTP_404_NOT_FOUND)

        now = timezone.now().date()
        if coupon.valid_from and coupon.valid_from > now:
            return Response({'exito': False, 'mensaje': 'Este cupón aún no es válido'}, status=status.HTTP_400_BAD_REQUEST)
        if coupon.valid_until and coupon.valid_until < now:
            return Response({'exito': False, 'mensaje': 'Este cupón ha expirado'}, status=status.HTTP_400_BAD_REQUEST)
        if coupon.max_uses and coupon.times_used >= coupon.max_uses:
            return Response({'exito': False, 'mensaje': 'Este cupón ha alcanzado su límite de usos'}, status=status.HTTP_400_BAD_REQUEST)

        total = Decimal(str(amount))
        if coupon.min_purchase_amount and total < coupon.min_purchase_amount:
            return Response({
                'exito': False,
                'mensaje': f'El monto mínimo para este cupón es S/ {coupon.min_purchase_amount}'
            }, status=status.HTTP_400_BAD_REQUEST)

        if coupon.discount_type == 'percentage':
            discount = total * (coupon.discount_value / 100)
            if coupon.max_discount_amount:
                discount = min(discount, coupon.max_discount_amount)
        else:
            discount = min(coupon.discount_value, total)

        return Response({
            'exito': True,
            'mensaje': f'Cupón aplicado: {coupon.description}',
            'coupon_id': coupon.id,
            'discount_type': coupon.discount_type,
            'discount_value': str(coupon.discount_value),
            'discount_amount': str(discount.quantize(Decimal('0.01'))),
            'final_amount': str((total - discount).quantize(Decimal('0.01'))),
        })


class WishlistViewSet(viewsets.ModelViewSet):
    """ViewSet para lista de deseos"""
    queryset = Wishlist.objects.select_related('package__destination')
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
        # Verificar si ya existe
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
