from rest_framework import serializers
from .models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'package', 'status', 'admin_response', 'inquiry_type',
            'destination_text', 'departure_date', 'return_date',
            'num_adults', 'num_children', 'budget', 'interests',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'admin_response', 'created_at', 'updated_at']
