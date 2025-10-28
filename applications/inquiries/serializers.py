from rest_framework import serializers
from .models import Inquiry

class InquirySerializer(serializers.ModelSerializer):
    """Serializer para el modelo Inquiry"""
    
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['created_at']
