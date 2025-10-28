from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer

# Create your views here.

class RegisterView(generics.CreateAPIView):
    """Registro de nuevos usuarios"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    """Inicio de sesión de usuarios"""
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Login endpoint - Implementar lógica de autenticación'})

class LogoutView(generics.GenericAPIView):
    """Cerrar sesión de usuarios"""
    def post(self, request, *args, **kwargs):
        return Response({'message': 'Logout exitoso'})

class ProfileView(generics.RetrieveUpdateAPIView):
    """Perfil del usuario actual"""
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """Lista de todos los usuarios"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
