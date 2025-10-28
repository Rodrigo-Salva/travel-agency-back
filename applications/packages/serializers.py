from rest_framework import serializers
from .models import Category, Package, Itinerary

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Category"""
    
    class Meta:
        model = Category
        fields = '__all__'

class ItinerarySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Itinerary"""
    
    class Meta:
        model = Itinerary
        fields = '__all__'

class PackageListSerializer(serializers.ModelSerializer):
    """Serializer para listar paquetes (campos resumidos)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    
    class Meta:
        model = Package
        fields = [
            'id', 'name', 'slug', 'category_name', 'destination_name',
            'duration_days', 'duration_nights', 'price_adult', 'price_child',
            'max_people', 'image', 'is_featured', 'is_active'
        ]

class PackageDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle de paquetes (con itinerarios anidados)"""
    category = CategorySerializer(read_only=True)
    destination = serializers.StringRelatedField(read_only=True)
    itineraries = ItinerarySerializer(many=True, read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'slug']
