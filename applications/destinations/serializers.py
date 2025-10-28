from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Destination"""
    
    class Meta:
        model = Destination
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
