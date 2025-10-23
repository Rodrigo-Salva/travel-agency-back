from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Coupon
from .serializers import CouponSerializer, CouponListSerializer, CouponValidateSerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'discount_type']
    search_fields = ['code', 'description']
    ordering_fields = ['created_at', 'valid_from', 'valid_until']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            today = timezone.now().date()
            queryset = queryset.filter(
                is_active=True,
                valid_from__lte=today,
                valid_until__gte=today
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CouponListSerializer
        elif self.action == 'validate_coupon':
            return CouponValidateSerializer
        return CouponSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
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
                'discount_value': coupon.discount_value,
                'discount_display': coupon.get_discount_display(),
            },
            'discount_amount': discount,
            'final_amount': purchase_amount - discount
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        coupon = self.get_object()
        coupon.use_coupon()
        
        serializer = self.get_serializer(coupon)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        today = timezone.now().date()
        active_coupons = self.get_queryset().filter(
            is_active=True,
            valid_from__lte=today,
            valid_until__gte=today
        )
        
        serializer = CouponListSerializer(active_coupons, many=True)
        return Response(serializer.data)