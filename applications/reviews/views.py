from django.shortcuts import render
from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.

class ReviewListView(generics.ListAPIView):
    """Lista todas las reseñas"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveAPIView):
    """Detalle de una reseña específica"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewCreateView(generics.CreateAPIView):
    """Crear una nueva reseña"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewUpdateView(generics.UpdateAPIView):
    """Actualizar una reseña"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDeleteView(generics.DestroyAPIView):
    """Eliminar una reseña"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewsByPackageView(generics.ListAPIView):
    """Reseñas por paquete"""
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        package_id = self.kwargs['package_id']
        return Review.objects.filter(package_id=package_id)

class ReviewsByHotelView(generics.ListAPIView):
    """Reseñas por hotel"""
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Review.objects.filter(hotel_id=hotel_id)

class MyReviewsView(generics.ListAPIView):
    """Mis reseñas"""
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
