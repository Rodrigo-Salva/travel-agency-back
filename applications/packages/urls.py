from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PackageViewSet, ItineraryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', PackageViewSet, basename='package')

# Rutas manuales para itinerario anidado bajo paquete:
# GET/POST  /api/packages/{package_pk}/itinerary/
# GET/PUT/PATCH/DELETE /api/packages/{package_pk}/itinerary/{pk}/
itinerary_list   = ItineraryViewSet.as_view({'get': 'list',   'post': 'create'})
itinerary_detail = ItineraryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('', include(router.urls)),
    path('<int:package_pk>/itinerary/', itinerary_list, name='package-itinerary-list'),
    path('<int:package_pk>/itinerary/<int:pk>/', itinerary_detail, name='package-itinerary-detail'),
]
