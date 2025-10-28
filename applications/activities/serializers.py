from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Activity"""
    
    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
