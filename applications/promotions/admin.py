from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'description',
        'discount_type',
        'discount_value',
        'valid_from',
        'valid_until',
        'times_used',
        'max_uses',
        'is_active',
    ]
    
    list_filter = [
        'discount_type',
        'is_active',
        'valid_from',
        'valid_until',
    ]
    
    search_fields = ['code', 'description']
    
    readonly_fields = ['times_used', 'created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Configuración de Descuento', {
            'fields': (
                'discount_type',
                'discount_value',
                'min_purchase_amount',
                'max_discount_amount'
            )
        }),
        ('Validez', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Límites de Uso', {
            'fields': ('max_uses', 'times_used')
        }),
        ('Información Adicional', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['activate_coupons', 'deactivate_coupons', 'reset_usage']
    
    def activate_coupons(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} cupón(es) activado(s) exitosamente.')
    activate_coupons.short_description = 'Activar cupones seleccionados'
    
    def deactivate_coupons(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} cupón(es) desactivado(s) exitosamente.')
    deactivate_coupons.short_description = 'Desactivar cupones seleccionados'
    
    def reset_usage(self, request, queryset):
        updated = queryset.update(times_used=0)
        self.message_user(request, f'Uso reiniciado para {updated} cupón(es).')
    reset_usage.short_description = 'Reiniciar contador de usos'