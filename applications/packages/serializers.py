from rest_framework import serializers
from .models import Category, Package, Itinerary, Wishlist
from applications.destinations.models import Destination


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías de paquetes"""
    packages_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'packages_count', 'created_at', 'updated_at']

    def get_packages_count(self, obj):
        return obj.packages.count()


class ItinerarySerializer(serializers.ModelSerializer):
    """Serializer para itinerarios"""
    
    class Meta:
        model = Itinerary
        fields = ['id', 'day_number', 'title', 'description', 'activities', 'meals_included', 'created_at', 'updated_at']


class PackageListSerializer(serializers.ModelSerializer):
    """Serializer para lista de paquetes (campos resumidos)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    destination_city = serializers.CharField(source='destination.city', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'slug', 'category_name', 'destination_name', 
            'destination_city', 'destination_country', 'short_description',
            'duration_days', 'duration_nights', 'price_adult', 'price_child',
            'max_people', 'min_people', 'includes', 'image_url', 'is_featured',
            'available_from', 'available_until', 'created_at'
        ]

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class PackageDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle de paquetes (con itinerario anidado)"""
    category = CategorySerializer(read_only=True)
    destination = serializers.SerializerMethodField()
    itineraries = ItinerarySerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'slug', 'category', 'destination', 'description',
            'short_description', 'duration_days', 'duration_nights',
            'price_adult', 'price_child', 'max_people', 'min_people',
            'includes', 'image_url', 'is_featured', 'available_from',
            'available_until', 'itineraries', 'created_at', 'updated_at'
        ]

    def get_destination(self, obj):
        return {
            'id': obj.destination.id,
            'name': obj.destination.name,
            'city': obj.destination.city,
            'country': obj.destination.country,
            'description': obj.destination.description,
            'short_description': obj.destination.short_description,
        }

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class WishlistSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'user',
            'package',
            'package_name',
            'package_description',
            'added_at',
        ]
        read_only_fields = ['id', 'user', 'added_at']
    
    def validate(self, data):
        request = self.context.get('request')
        package = data.get('package')
        
        if request and request.user and package:
            if Wishlist.objects.filter(user=request.user, package=package).exists():
                raise serializers.ValidationError(
                    "Este paquete ya está en tu lista de deseos"
                )
        
        return data


class WishlistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['package']


class WishlistListSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = [
            'id',
            'package',
            'package_name',
            'added_at',
        ]