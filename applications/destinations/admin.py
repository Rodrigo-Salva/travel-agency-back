from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'continent', 'is_popular', 'best_season')
    search_fields = ('name', 'country', 'continent')
    list_filter = ('continent', 'is_popular')
