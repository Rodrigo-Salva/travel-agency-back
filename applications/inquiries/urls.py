"""
URLs de Consultas
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de consultas
    path('', views.InquiryListView.as_view(), name='inquiry-list'),
    path('<int:pk>/', views.InquiryDetailView.as_view(), name='inquiry-detail'),
    path('create/', views.InquiryCreateView.as_view(), name='inquiry-create'),
    path('<int:pk>/update/', views.InquiryUpdateView.as_view(), name='inquiry-update'),
    path('<int:pk>/delete/', views.InquiryDeleteView.as_view(), name='inquiry-delete'),
    path('my-inquiries/', views.MyInquiriesView.as_view(), name='my-inquiries'),
    path('respond/<int:pk>/', views.RespondInquiryView.as_view(), name='respond-inquiry'),
]
