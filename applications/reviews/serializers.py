from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Review"""
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
