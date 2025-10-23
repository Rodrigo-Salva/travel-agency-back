from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PackageViewSet, WishlistViewSet

# Crear router para las APIs
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]
