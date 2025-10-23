from rest_framework import serializers
from .models import Hotel
from applications.destinations.models import Destination
from applications.destinations.serializers import DestinationSerializer

class HotelSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset = Destination.objects.all(),
        source='destination',
        write_only=True
    )

    class Meta:
        model = Hotel
        fields = [
            'id',
            'name',
            'destination',
            'destination_id',
            'address',
            'star_rating',
            'description',
            'amenities',
            'check_in_time',
            'check_out_time',
            'phone',
            'email',
            'price_per_night',
            'total_rooms',
            'image',
            'is_active',
        ]