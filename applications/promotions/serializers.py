from rest_framework import serializers
from applications.promotions.models import Coupon, Wishlist


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['times_used', 'created_at']


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


class WishlistSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_price = serializers.DecimalField(source='package.price_adult', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'package', 'package_name', 'package_price', 'added_at']
        read_only_fields = ['id', 'added_at']