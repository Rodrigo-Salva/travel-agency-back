"""
URLs de Reservas
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de reservas
    path('', views.BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('create/', views.BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking-update'),
    path('<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking-delete'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),
    path('confirm/<int:pk>/', views.ConfirmBookingView.as_view(), name='confirm-booking'),
    path('cancel/<int:pk>/', views.CancelBookingView.as_view(), name='cancel-booking'),
]
