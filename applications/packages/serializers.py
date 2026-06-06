from rest_framework import serializers
from .models import Category, Package, Itinerary


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorías
    """
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']


class ItinerarySerializer(serializers.ModelSerializer):
    """
    Serializer para itinerarios
    """
    
    class Meta:
        model = Itinerary
        fields = [
            'id',
            'day_number',
            'title',
            'description',
            'activities',
            'meals_included'
        ]


class PackageListSerializer(serializers.ModelSerializer):
    """
    Serializer para listado de paquetes (información resumida)
    """
    
    destination_name = serializers.CharField(
        source='destination.name',
        read_only=True
    )
    
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    
    available_spots = serializers.ReadOnlyField()
    is_sold_out = serializers.ReadOnlyField()

    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'slug',
            'category_name',
            'destination_name',
            'short_description',
            'duration_days',
            'duration_nights',
            'price_adult',
            'price_child',
            'image',
            'is_featured',
            'discount_percentage',
            'discounted_price_adult',
            'capacity',
            'booked_count',
            'available_spots',
            'is_sold_out',
            'created_at'
        ]


class PackageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer detallado de paquete con itinerario completo
    """

    destination = serializers.StringRelatedField()
    destination_id = serializers.IntegerField(source='destination.id', read_only=True)
    destination_country = serializers.CharField(source='destination.country', read_only=True)
    destination_latitude = serializers.DecimalField(source='destination.latitude', max_digits=9, decimal_places=6, read_only=True)
    destination_longitude = serializers.DecimalField(source='destination.longitude', max_digits=9, decimal_places=6, read_only=True)
    category = CategorySerializer(read_only=True)
    itinerary = ItinerarySerializer(many=True, read_only=True)

    # Campos calculados
    total_duration = serializers.SerializerMethodField()
    discounted_price_adult = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()
    is_sold_out = serializers.ReadOnlyField()

    class Meta:
        model = Package
        fields = [
            'id',
            'name',
            'slug',
            'category',
            'destination',
            'destination_id',
            'destination_country',
            'destination_latitude',
            'destination_longitude',
            'description',
            'short_description',
            'duration_days',
            'duration_nights',
            'total_duration',
            'price_adult',
            'price_child',
            'discount_percentage',
            'discounted_price_adult',
            'max_people',
            'min_people',
            'includes_flight',
            'includes_hotel',
            'includes_meals',
            'includes_transport',
            'includes_guide',
            'image',
            'is_active',
            'is_featured',
            'available_from',
            'available_until',
            'itinerary',
            'capacity',
            'booked_count',
            'available_spots',
            'is_sold_out',
            'created_at',
            'updated_at'
        ]

    def get_total_duration(self, obj):
        """Calcular duración total como string"""
        return f"{obj.duration_days} días / {obj.duration_nights} noches"


class PackageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear paquetes
    """
    
    class Meta:
        model = Package
        fields = [
            'name',
            'slug',
            'category',
            'destination',
            'description',
            'short_description',
            'duration_days',
            'duration_nights',
            'price_adult',
            'price_child',
            'max_people',
            'min_people',
            'includes_flight',
            'includes_hotel',
            'includes_meals',
            'includes_transport',
            'includes_guide',
            'image',
            'is_featured',
            'discount_percentage',
            'capacity',
            'available_from',
            'available_until'
        ]

    def validate(self, attrs):
        """Validaciones personalizadas"""
        if attrs.get('duration_days', 0) < 1:
            raise serializers.ValidationError({
                "duration_days": "La duración debe ser al menos 1 día"
            })
        
        if attrs.get('duration_nights', 0) < 0:
            raise serializers.ValidationError({
                "duration_nights": "Las noches no pueden ser negativas"
            })
        
        if attrs.get('price_adult', 0) <= 0:
            raise serializers.ValidationError({
                "price_adult": "El precio debe ser mayor a 0"
            })
        
        if attrs.get('max_people', 0) < attrs.get('min_people', 1):
            raise serializers.ValidationError({
                "max_people": "El máximo debe ser mayor o igual al mínimo"
            })
        
        return attrs
