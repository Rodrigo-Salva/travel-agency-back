from django.contrib import admin

from . import models


class PassengerInline(admin.TabularInline):
	model = models.Passenger
	extra = 0


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
	inlines = [PassengerInline]
	list_display = ('booking_number', 'get_customer_email', 'total_amount', 'status', 'payment_status', 'booking_date')
	list_filter = ('status', 'booking_date')
	search_fields = ('booking_number',)

	def get_customer_email(self, obj):
		return obj.customer.email if obj.customer else 'N/A'
	get_customer_email.short_description = 'Customer'


@admin.register(models.Passenger)
class PassengerAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'passenger_type', 'booking')
	search_fields = ('first_name', 'last_name', 'passport_number')

