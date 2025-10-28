from django.shortcuts import render
from rest_framework import generics
from .models import Promotion
from .serializers import PromotionSerializer

# Create your views here.

class PromotionListView(generics.ListAPIView):
    """Lista todas las promociones"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionDetailView(generics.RetrieveAPIView):
    """Detalle de una promoción específica"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionCreateView(generics.CreateAPIView):
    """Crear una nueva promoción"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionUpdateView(generics.UpdateAPIView):
    """Actualizar una promoción"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionDeleteView(generics.DestroyAPIView):
    """Eliminar una promoción"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class ActivePromotionsView(generics.ListAPIView):
    """Promociones activas"""
    serializer_class = PromotionSerializer
    
    def get_queryset(self):
        from django.utils import timezone
        now = timezone.now().date()
        return Promotion.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now)

class PromotionsByTypeView(generics.ListAPIView):
    """Promociones por tipo"""
    serializer_class = PromotionSerializer
    
    def get_queryset(self):
        promotion_type = self.kwargs['promotion_type']
        return Promotion.objects.filter(promotion_type__icontains=promotion_type)
