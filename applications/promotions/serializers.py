from rest_framework import serializers
from .models import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Promotion"""
    
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
