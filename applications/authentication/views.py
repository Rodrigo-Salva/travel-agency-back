import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdminUser
from .emails import send_password_reset, send_password_changed
from .models import Notification
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    NotificationSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer personalizado para incluir datos del usuario"""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar información del usuario al response
        data['usuario'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'nombre_completo': f"{self.user.first_name} {self.user.last_name}",
            'tipo_usuario': self.user.user_type,
        }
        
        return data


class LoginView(TokenObtainPairView):
    """POST /api/v1/auth/login/ - Login con JWT"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            return Response({
                'exito': True,
                'mensaje': '¡Bienvenido de nuevo!',
                'access': response.data.get('access'),
                'refresh': response.data.get('refresh'),
                'usuario': response.data.get('usuario')
            })
        except Exception as e:
            return Response({
                'exito': False,
                'mensaje': 'Usuario o contraseña incorrectos',
                'detalles': 'Verifica tus credenciales e intenta nuevamente'
            }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/ - Registro público"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Por favor verifica los datos ingresados',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        return Response({
            'exito': True,
            'mensaje': '¡Registro exitoso! Tu cuenta ha sido creada',
            'usuario': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de usuarios"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'create', 'update', 'partial_update', 'destroy', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        user_type = self.request.query_params.get('user_type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'exito': True,
                'mensaje': f'Se encontraron {queryset.count()} usuarios',
                'usuarios': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'exito': True,
            'mensaje': f'Se encontraron {queryset.count()} usuarios',
            'usuarios': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """GET /api/v1/auth/users/me/ - Perfil del usuario autenticado"""
        serializer = self.get_serializer(request.user)
        return Response({
            'exito': True,
            'mensaje': 'Perfil obtenido correctamente',
            'usuario': serializer.data
        })
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """PUT/PATCH /api/v1/auth/users/update_profile/ - Actualizar perfil"""
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if not serializer.is_valid():
            return Response({
                'exito': False,
                'mensaje': 'Error al actualizar el perfil',
                'errores': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        return Response({
            'exito': True,
            'mensaje': 'Tu perfil ha sido actualizado exitosamente',
            'usuario': UserSerializer(request.user).data
        })
    
    def destroy(self, request, *args, **kwargs):
        """DELETE /api/v1/auth/users/{id}/ - Desactivar usuario"""
        instance = self.get_object()
        
        if not instance.is_active:
            return Response({
                'exito': False,
                'mensaje': 'Este usuario ya está desactivado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        instance.is_active = False
        instance.save()
        
        return Response({
            'exito': True,
            'mensaje': 'Usuario desactivado exitosamente'
        })


class ChangePasswordView(APIView):
    """POST /api/auth/change_password/ — cambiar contraseña estando autenticado"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({'exito': False, 'mensaje': 'La contraseña actual es incorrecta.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        send_password_changed(user)
        return Response({'exito': True, 'mensaje': 'Contraseña actualizada correctamente.'})


class ForgotPasswordView(APIView):
    """POST /api/auth/forgot_password/ — solicitar enlace de reset"""
    permission_classes = [AllowAny]
    _EXPIRY = 30 * 60  # 30 minutos en segundos

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email'].lower().strip()
        # Respuesta idéntica exista o no el usuario (evita user enumeration)
        generic = {'exito': True,
                   'mensaje': 'Si el correo está registrado recibirás un enlace en los próximos minutos.'}

        User = get_user_model()
        try:
            user = User.objects.get(email__iexact=email, is_active=True)
        except User.DoesNotExist:
            return Response(generic)

        token = secrets.token_urlsafe(48)
        cache.set(f'pwd_reset:{token}', user.pk, self._EXPIRY)

        frontend_url = request.data.get('frontend_url', 'http://localhost:3000')
        reset_url = f"{frontend_url}/reset-password?token={token}"
        send_password_reset(user, reset_url)

        return Response(generic)


class ResetPasswordView(APIView):
    """POST /api/auth/reset_password/ — confirmar reset con token"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'exito': False, 'errores': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        user_pk = cache.get(f'pwd_reset:{token}')

        if not user_pk:
            return Response({'exito': False,
                             'mensaje': 'El enlace es inválido o ha expirado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_pk, is_active=True)
        except User.DoesNotExist:
            return Response({'exito': False, 'mensaje': 'Usuario no encontrado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        cache.delete(f'pwd_reset:{token}')
        send_password_changed(user)

        return Response({'exito': True,
                         'mensaje': '¡Contraseña restablecida! Ya puedes iniciar sesión.'})


class NotificationViewSet(viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def list(self, request):
        """GET /api/auth/notifications/ — lista las 20 más recientes"""
        qs = self.get_queryset()[:20]
        unread = self.get_queryset().filter(is_read=False).count()
        return Response({
            'exito': True,
            'unread': unread,
            'notifications': NotificationSerializer(qs, many=True).data,
        })

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """POST /api/auth/notifications/mark_all_read/"""
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'exito': True, 'mensaje': 'Notificaciones marcadas como leídas.'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """POST /api/auth/notifications/{id}/mark_read/"""
        notif = self.get_queryset().filter(pk=pk).first()
        if notif:
            notif.is_read = True
            notif.save(update_fields=['is_read'])
        return Response({'exito': True})
