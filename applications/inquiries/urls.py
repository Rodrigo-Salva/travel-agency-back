from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InquiryViewSet

app_name = 'inquiries'

router = DefaultRouter()
router.register(r'inquiries', InquiryViewSet, basename='inquiry')

urlpatterns = [
    path('', include(router.urls)),
]