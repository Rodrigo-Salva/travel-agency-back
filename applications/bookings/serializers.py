from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Booking"""
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'booking_date']
