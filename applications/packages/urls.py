"""
URLs de Paquetes Turísticos
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear router para ViewSets
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'itineraries', views.ItineraryViewSet)
router.register(r'', views.PackageViewSet)

urlpatterns = [
    # URLs del router (ViewSets)
    path('', include(router.urls)),
]
