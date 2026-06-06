from django.contrib import admin
from .models import WhatsAppContact, WhatsAppConversation, WhatsAppMessage, WhatsAppCampaign


@admin.register(WhatsAppContact)
class WhatsAppContactAdmin(admin.ModelAdmin):
    list_display = ['phone', 'name', 'created_at']
    search_fields = ['phone', 'name']


@admin.register(WhatsAppConversation)
class WhatsAppConversationAdmin(admin.ModelAdmin):
    list_display = ['contact', 'last_message_at', 'unread_count']
    list_filter = ['last_message_at']


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'direction', 'status', 'scheduled_at', 'sent_at', 'created_at']
    list_filter = ['direction', 'status']
    search_fields = ['content', 'conversation__contact__phone']


@admin.register(WhatsAppCampaign)
class WhatsAppCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'delay_between_ms', 'created_by', 'created_at']
    list_filter = ['status']
    filter_horizontal = ['contacts']
