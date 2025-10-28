from django.shortcuts import render
from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer

# Create your views here.

class ActivityListView(generics.ListAPIView):
    """Lista todas las actividades"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityDetailView(generics.RetrieveAPIView):
    """Detalle de una actividad específica"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityCreateView(generics.CreateAPIView):
    """Crear una nueva actividad"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityUpdateView(generics.UpdateAPIView):
    """Actualizar una actividad"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivityDeleteView(generics.DestroyAPIView):
    """Eliminar una actividad"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ActivitySearchView(generics.ListAPIView):
    """Buscar actividades"""
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Activity.objects.filter(name__icontains=query)

class ActivitiesByDestinationView(generics.ListAPIView):
    """Actividades por destino"""
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        destination_id = self.kwargs['destination_id']
        return Activity.objects.filter(destination_id=destination_id)

class ActivitiesByCategoryView(generics.ListAPIView):
    """Actividades por categoría"""
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        category = self.kwargs['category']
        return Activity.objects.filter(category__icontains=category)
