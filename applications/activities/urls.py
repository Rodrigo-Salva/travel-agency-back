"""
URLs de Actividades
"""
from django.urls import path
from . import views

urlpatterns = [
    # Gestión de actividades
    path('', views.ActivityListView.as_view(), name='activity-list'),
    path('<int:pk>/', views.ActivityDetailView.as_view(), name='activity-detail'),
    path('create/', views.ActivityCreateView.as_view(), name='activity-create'),
    path('<int:pk>/update/', views.ActivityUpdateView.as_view(), name='activity-update'),
    path('<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity-delete'),
    path('search/', views.ActivitySearchView.as_view(), name='activity-search'),
    path('by-destination/<int:destination_id>/', views.ActivitiesByDestinationView.as_view(), name='activities-by-destination'),
    path('by-category/<str:category>/', views.ActivitiesByCategoryView.as_view(), name='activities-by-category'),
]
