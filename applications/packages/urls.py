from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PackageViewSet

# Crear router para las APIs
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'packages', PackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
