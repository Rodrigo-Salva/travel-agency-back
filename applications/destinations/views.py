from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Destination
from .serializers import DestinationSerializer

# Create your views here.

class DestinationListView(generics.ListAPIView):
    """Lista todos los destinos"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDetailView(generics.RetrieveAPIView):
    """Detalle de un destino específico"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationCreateView(generics.CreateAPIView):
    """Crear un nuevo destino"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationUpdateView(generics.UpdateAPIView):
    """Actualizar un destino"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationDeleteView(generics.DestroyAPIView):
    """Eliminar un destino"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DestinationSearchView(generics.ListAPIView):
    """Buscar destinos"""
    serializer_class = DestinationSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Destination.objects.filter(name__icontains=query)

class PopularDestinationsView(generics.ListAPIView):
    """Destinos populares"""
    serializer_class = DestinationSerializer
    
    def get_queryset(self):
        return Destination.objects.all()[:5]  # Top 5 destinos
