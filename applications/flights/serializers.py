from rest_framework import serializers
from .models import Flight

class FlightSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Flight"""
    
    class Meta:
        model = Flight
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
