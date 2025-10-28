from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Hotel"""
    
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
