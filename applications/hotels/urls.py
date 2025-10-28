"""
URLs de Hoteles
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de hoteles
    path('', views.HotelListView.as_view(), name='hotel-list'),
    path('<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('create/', views.HotelCreateView.as_view(), name='hotel-create'),
    path('<int:pk>/update/', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel-delete'),
    path('search/', views.HotelSearchView.as_view(), name='hotel-search'),
    path('by-destination/<int:destination_id>/', views.HotelsByDestinationView.as_view(), name='hotels-by-destination'),
    path('by-rating/<int:rating>/', views.HotelsByRatingView.as_view(), name='hotels-by-rating'),
]
