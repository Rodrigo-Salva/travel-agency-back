from django.shortcuts import render
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer

# Create your views here.

class BookingListView(generics.ListAPIView):
    """Lista todas las reservas"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveAPIView):
    """Detalle de una reserva específica"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingCreateView(generics.CreateAPIView):
    """Crear una nueva reserva"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingUpdateView(generics.UpdateAPIView):
    """Actualizar una reserva"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDeleteView(generics.DestroyAPIView):
    """Eliminar una reserva"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class MyBookingsView(generics.ListAPIView):
    """Mis reservas"""
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class ConfirmBookingView(generics.UpdateAPIView):
    """Confirmar reserva"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = 'confirmed'
        booking.save()
        return Response({'message': 'Reserva confirmada'})

class CancelBookingView(generics.UpdateAPIView):
    """Cancelar reserva"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.status = 'cancelled'
        booking.save()
        return Response({'message': 'Reserva cancelada'})
