from rest_framework import serializers
from django.utils import timezone
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    discount_display = serializers.CharField(source='get_discount_display', read_only=True)
    
    class Meta:
        model = Coupon
        fields = [
            'id',
            'code',
            'description',
            'discount_type',
            'discount_value',
            'discount_display',
            'min_purchase_amount',
            'max_discount_amount',
            'valid_from',
            'valid_until',
            'max_uses',
            'times_used',
            'is_active',
            'is_valid',
            'created_at',
        ]
        read_only_fields = ['id', 'times_used', 'created_at']
    
    def validate_code(self, value):
        value = value.upper().strip()
        if len(value) < 3:
            raise serializers.ValidationError("El código debe tener al menos 3 caracteres")
        return value
    
    def validate(self, data):
        if data.get('valid_from') and data.get('valid_until'):
            if data['valid_from'] > data['valid_until']:
                raise serializers.ValidationError(
                    "La fecha de inicio no puede ser posterior a la fecha de fin"
                )
        
        if data.get('discount_type') == 'percentage':
            if data.get('discount_value', 0) > 100:
                raise serializers.ValidationError(
                    "El porcentaje de descuento no puede ser mayor a 100"
                )
        
        return data


class CouponListSerializer(serializers.ModelSerializer):
    discount_display = serializers.CharField(source='get_discount_display', read_only=True)
    
    class Meta:
        model = Coupon
        fields = [
            'id',
            'code',
            'description',
            'discount_display',
            'valid_from',
            'valid_until',
            'is_active',
        ]


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    purchase_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate_code(self, value):
        return value.upper().strip()
    
    def validate(self, data):
        try:
            coupon = Coupon.objects.get(code=data['code'])
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("Cupón no válido")
        
        if not coupon.can_be_used(data['purchase_amount']):
            if not coupon.is_valid():
                raise serializers.ValidationError("Este cupón ha expirado o no está activo")
            if coupon.min_purchase_amount and data['purchase_amount'] < coupon.min_purchase_amount:
                raise serializers.ValidationError(
                    f"El monto mínimo de compra es ${coupon.min_purchase_amount}"
                )
        
        data['coupon'] = coupon
        return data