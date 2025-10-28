"""
URLs de Reseñas
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de reseñas
    path('', views.ReviewListView.as_view(), name='review-list'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review-update'),
    path('<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review-delete'),
    path('by-package/<int:package_id>/', views.ReviewsByPackageView.as_view(), name='reviews-by-package'),
    path('by-hotel/<int:hotel_id>/', views.ReviewsByHotelView.as_view(), name='reviews-by-hotel'),
    path('my-reviews/', views.MyReviewsView.as_view(), name='my-reviews'),
]
