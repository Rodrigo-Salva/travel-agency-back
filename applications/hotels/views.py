from django.shortcuts import render
from rest_framework import generics
from .models import Hotel
from .serializers import HotelSerializer

# Create your views here.

class HotelListView(generics.ListAPIView):
    """Lista todos los hoteles"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelDetailView(generics.RetrieveAPIView):
    """Detalle de un hotel específico"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelCreateView(generics.CreateAPIView):
    """Crear un nuevo hotel"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelUpdateView(generics.UpdateAPIView):
    """Actualizar un hotel"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelDeleteView(generics.DestroyAPIView):
    """Eliminar un hotel"""
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelSearchView(generics.ListAPIView):
    """Buscar hoteles"""
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Hotel.objects.filter(name__icontains=query)

class HotelsByDestinationView(generics.ListAPIView):
    """Hoteles por destino"""
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        destination_id = self.kwargs['destination_id']
        return Hotel.objects.filter(destination_id=destination_id)

class HotelsByRatingView(generics.ListAPIView):
    """Hoteles por calificación"""
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        rating = self.kwargs['rating']
        return Hotel.objects.filter(rating=rating)
