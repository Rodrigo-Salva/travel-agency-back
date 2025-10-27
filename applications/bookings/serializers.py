from uuid import uuid4

from rest_framework import serializers

from . import models


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Passenger
        fields = [
            'id',
            'passenger_type',
            'title',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'passport_number',
            'nationality',
        ]


class HotelBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HotelBooking
        fields = [
            'id',
            'hotel',
            'check_in_date',
            'check_out_date',
            'num_rooms',
            'room_type',
            'price_per_night',
            'total_nights',
            'total_price',
            'confirmation_number',
        ]


class FlightBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlightBooking
        fields = [
            'id',
            'flight',
            'booking_type',
            'num_passengers',
            'seat_numbers',
            'price_per_person',
            'total_price',
            'pnr_number',
        ]


class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = [
            'id',
            'booking_number',
            'customer',
            'travel_date',
            'return_date',
            'num_adults',
            'num_children',
            'num_infants',
            'total_amount',
            'status',
            'payment_status',
            'booking_date',
        ]


class BookingDetailSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, read_only=True)
    hotel_bookings = HotelBookingSerializer(many=True, read_only=True)
    flight_bookings = FlightBookingSerializer(many=True, read_only=True)

    class Meta:
        model = models.Booking
        fields = '__all__'


class BookingCreateSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True, required=False)
    hotel_bookings = HotelBookingSerializer(many=True, required=False)
    flight_bookings = FlightBookingSerializer(many=True, required=False)

    class Meta:
        model = models.Booking
        fields = [
            'id',
            'booking_number',
            'customer',
            'package',
            'travel_date',
            'return_date',
            'num_adults',
            'num_children',
            'num_infants',
            'subtotal',
            'discount_amount',
            'tax_amount',
            'total_amount',
            'paid_amount',
            'status',
            'payment_status',
            'special_requests',
            'booking_date',
            'updated_at',
            'passengers',
            'hotel_bookings',
            'flight_bookings',
        ]
        read_only_fields = ['id', 'booking_date', 'updated_at', 'customer']
        extra_kwargs = {
            'booking_number': {'required': False, 'allow_blank': True},
        }

    def validate(self, attrs):
        from datetime import date

        travel_date = attrs.get('travel_date')
        return_date = attrs.get('return_date')

        if travel_date and travel_date < date.today():
            raise serializers.ValidationError({
                'travel_date': 'La fecha de viaje no puede ser en el pasado.'
            })
        
        if return_date and travel_date and return_date <= travel_date:
            raise serializers.ValidationError({
                'return_date': 'La fecha de regreso debe ser posterior a la fecha de viaje.'
            })
        
        return attrs

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers', [])
        hotel_bookings_data = validated_data.pop('hotel_bookings', [])
        flight_bookings_data = validated_data.pop('flight_bookings', [])

        if not validated_data.get('booking_number'):
            validated_data['booking_number'] = uuid4().hex[:12].upper()

        booking = models.Booking.objects.create(**validated_data)

        for p in passengers_data:
            models.Passenger.objects.create(booking=booking, **p)

        for h in hotel_bookings_data:
            models.HotelBooking.objects.create(booking=booking, **h)

        for f in flight_bookings_data:
            models.FlightBooking.objects.create(booking=booking, **f)

        return booking
