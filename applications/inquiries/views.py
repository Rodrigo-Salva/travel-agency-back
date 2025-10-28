from django.shortcuts import render
from rest_framework import generics
from .models import Inquiry
from .serializers import InquirySerializer

# Create your views here.

class InquiryListView(generics.ListAPIView):
    """Lista todas las consultas"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class InquiryDetailView(generics.RetrieveAPIView):
    """Detalle de una consulta específica"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class InquiryCreateView(generics.CreateAPIView):
    """Crear una nueva consulta"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class InquiryUpdateView(generics.UpdateAPIView):
    """Actualizar una consulta"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class InquiryDeleteView(generics.DestroyAPIView):
    """Eliminar una consulta"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

class MyInquiriesView(generics.ListAPIView):
    """Mis consultas"""
    serializer_class = InquirySerializer
    
    def get_queryset(self):
        return Inquiry.objects.filter(email=self.request.user.email)

class RespondInquiryView(generics.UpdateAPIView):
    """Responder consulta"""
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    
    def update(self, request, *args, **kwargs):
        inquiry = self.get_object()
        inquiry.is_responded = True
        inquiry.save()
        return Response({'message': 'Consulta marcada como respondida'})
