from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from .models import Inquiry
from .serializers import (
    InquirySerializer,
    InquiryListSerializer,
    InquiryCreateSerializer,
    InquiryResponseSerializer
)


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'package']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_staff:
            return queryset.none()
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InquiryCreateSerializer
        elif self.action == 'list':
            return InquiryListSerializer
        elif self.action == 'respond':
            return InquiryResponseSerializer
        return InquirySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(
            {
                'message': 'Consulta enviada exitosamente. Nos pondremos en contacto pronto.',
                'inquiry_id': serializer.data.get('id')
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def respond(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos para responder consultas'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        inquiry = self.get_object()
        serializer = InquiryResponseSerializer(inquiry, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(InquirySerializer(inquiry).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        inquiry = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Inquiry.STATUS_CHOICES):
            return Response(
                {'error': 'Estado inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inquiry.status = new_status
        inquiry.save()
        
        serializer = self.get_serializer(inquiry)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def by_status(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        status_param = request.query_params.get('status', 'new')
        inquiries = self.get_queryset().filter(status=status_param)
        
        serializer = InquiryListSerializer(inquiries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permisos'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from django.db.models import Count
        
        stats = self.get_queryset().values('status').annotate(count=Count('id'))
        
        return Response({
            'total': self.get_queryset().count(),
            'by_status': list(stats)
        })