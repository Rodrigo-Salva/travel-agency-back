from rest_framework import serializers
from .models import Coupon, Wishlist


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['times_used', 'created_at']


class WishlistSerializer(serializers.ModelSerializer):
    package_name        = serializers.CharField(source='package.name', read_only=True)
    package_price       = serializers.DecimalField(source='package.price_adult', max_digits=10, decimal_places=2, read_only=True)
    package_image       = serializers.ImageField(source='package.image', read_only=True)
    package_destination = serializers.CharField(source='package.destination.name', read_only=True)
    package_duration    = serializers.IntegerField(source='package.duration_days', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'package', 'package_name', 'package_price',
                  'package_image', 'package_destination', 'package_duration', 'added_at']
        read_only_fields = ['id', 'user', 'added_at',
                            'package_name', 'package_price',
                            'package_image', 'package_destination', 'package_duration']
