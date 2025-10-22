from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'country': {'required': True},
        }
