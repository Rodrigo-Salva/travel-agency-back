from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminUser
from .models import Inquiry
from .serializers import InquirySerializer


class InquiryViewSet(viewsets.ModelViewSet):
    """ViewSet para consultas"""
    queryset = Inquiry.objects.all().order_by('-created_at')
    serializer_class = InquirySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'inquiry_type']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'exito': True,
                'mensaje': f'Hay {queryset.count()} consultas',
                'consultas': serializer.data
            })
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Hay {queryset.count()} consultas',
            'consultas': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Error al enviar la consulta',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        
        return Response({
            'exito': True,
            'mensaje': '¡Tu consulta ha sido enviada! Te responderemos pronto',
            'consulta': serializer.data
        }, status=status.HTTP_201_CREATED)