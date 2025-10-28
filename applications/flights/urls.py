"""
URLs de Vuelos
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de vuelos
    path('', views.FlightListView.as_view(), name='flight-list'),
    path('<int:pk>/', views.FlightDetailView.as_view(), name='flight-detail'),
    path('create/', views.FlightCreateView.as_view(), name='flight-create'),
    path('<int:pk>/update/', views.FlightUpdateView.as_view(), name='flight-update'),
    path('<int:pk>/delete/', views.FlightDeleteView.as_view(), name='flight-delete'),
    path('search/', views.FlightSearchView.as_view(), name='flight-search'),
    path('by-route/', views.FlightsByRouteView.as_view(), name='flights-by-route'),
    path('available/', views.AvailableFlightsView.as_view(), name='available-flights'),
]
