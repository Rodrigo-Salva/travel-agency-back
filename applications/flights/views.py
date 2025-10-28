from django.shortcuts import render
from rest_framework import generics
from .models import Flight
from .serializers import FlightSerializer

# Create your views here.

class FlightListView(generics.ListAPIView):
    """Lista todos los vuelos"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightDetailView(generics.RetrieveAPIView):
    """Detalle de un vuelo específico"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightCreateView(generics.CreateAPIView):
    """Crear un nuevo vuelo"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightUpdateView(generics.UpdateAPIView):
    """Actualizar un vuelo"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightDeleteView(generics.DestroyAPIView):
    """Eliminar un vuelo"""
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

class FlightSearchView(generics.ListAPIView):
    """Buscar vuelos"""
    serializer_class = FlightSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Flight.objects.filter(flight_number__icontains=query)

class FlightsByRouteView(generics.ListAPIView):
    """Vuelos por ruta"""
    serializer_class = FlightSerializer
    
    def get_queryset(self):
        origin = self.request.query_params.get('origin', '')
        destination = self.request.query_params.get('destination', '')
        return Flight.objects.filter(origin__icontains=origin, destination__icontains=destination)

class AvailableFlightsView(generics.ListAPIView):
    """Vuelos disponibles"""
    serializer_class = FlightSerializer
    
    def get_queryset(self):
        return Flight.objects.filter(is_active=True)
