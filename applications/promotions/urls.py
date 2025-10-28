"""
URLs de Promociones
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de promociones
    path('', views.PromotionListView.as_view(), name='promotion-list'),
    path('<int:pk>/', views.PromotionDetailView.as_view(), name='promotion-detail'),
    path('create/', views.PromotionCreateView.as_view(), name='promotion-create'),
    path('<int:pk>/update/', views.PromotionUpdateView.as_view(), name='promotion-update'),
    path('<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion-delete'),
    path('active/', views.ActivePromotionsView.as_view(), name='active-promotions'),
    path('by-type/<str:promotion_type>/', views.PromotionsByTypeView.as_view(), name='promotions-by-type'),
]
