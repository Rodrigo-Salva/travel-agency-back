from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WAHAWebhookView,
    DeliveryCallbackView,
    ConversationViewSet,
    SendMessageView,
    CancelMessageView,
    WhatsAppCampaignViewSet,
    QueueStatsView,
    SessionStatusView,
    SessionStartView,
    SessionQRView,
    SessionLogoutView,
)

router = DefaultRouter()
router.register('conversations', ConversationViewSet, basename='wa-conversation')
router.register('campaigns', WhatsAppCampaignViewSet, basename='wa-campaign')

urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', WAHAWebhookView.as_view(), name='wa-webhook'),
    path('delivery/', DeliveryCallbackView.as_view(), name='wa-delivery'),
    path('send/', SendMessageView.as_view(), name='wa-send'),
    path('messages/<int:pk>/cancel/', CancelMessageView.as_view(), name='wa-cancel'),
    path('queue/stats/', QueueStatsView.as_view(), name='wa-stats'),
    path('session/', SessionStatusView.as_view(), name='wa-session-status'),
    path('session/start/', SessionStartView.as_view(), name='wa-session-start'),
    path('session/qr/', SessionQRView.as_view(), name='wa-session-qr'),
    path('session/logout/', SessionLogoutView.as_view(), name='wa-session-logout'),
]
