"""
URLs de [NOMBRE_APP]
EQUIPO X: Agregar las rutas aquí
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, UserViewSet, LoginView, NotificationViewSet,
    ChangePasswordView, ForgotPasswordView, ResetPasswordView,
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset-password'),
]
