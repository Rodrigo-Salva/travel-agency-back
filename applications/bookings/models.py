from decimal import Decimal

from django.conf import settings
from django.db import models


class Booking(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_CONFIRMED = 'confirmed'
	STATUS_CANCELLED = 'cancelled'
	STATUS_COMPLETED = 'completed'

	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pendiente'),
		(STATUS_CONFIRMED, 'Confirmada'),
		(STATUS_CANCELLED, 'Cancelada'),
		(STATUS_COMPLETED, 'Completada'),
	]

	PAYMENT_UNPAID = 'unpaid'
	PAYMENT_PARTIAL = 'partial'
	PAYMENT_PAID = 'paid'
	PAYMENT_REFUNDED = 'refunded'

	PAYMENT_STATUS_CHOICES = [
		(PAYMENT_UNPAID, 'No pagado'),
		(PAYMENT_PARTIAL, 'Pago parcial'),
		(PAYMENT_PAID, 'Pagado'),
		(PAYMENT_REFUNDED, 'Reembolsado'),
	]

	booking_number = models.CharField(max_length=64, unique=True, verbose_name='Número de reserva')
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name='Cliente')
	package = models.ForeignKey('packages.Package', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings', verbose_name='Paquete')
	travel_date = models.DateField(null=True, blank=True, verbose_name='Fecha de viaje')
	return_date = models.DateField(null=True, blank=True, verbose_name='Fecha de regreso')
	num_adults = models.PositiveIntegerField(default=1, verbose_name='Número de adultos')
	num_children = models.PositiveIntegerField(default=0, verbose_name='Número de niños')
	num_infants = models.PositiveIntegerField(default=0, verbose_name='Número de infantes')
	subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Subtotal')
	discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Descuento')
	tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Impuestos')
	total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Monto total')
	paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Monto pagado')
	status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Estado')
	payment_status = models.CharField(max_length=16, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_UNPAID, verbose_name='Estado de pago')
	special_requests = models.TextField(null=True, blank=True, verbose_name='Solicitudes especiales')
	booking_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de reserva')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

	class Meta:
		db_table = 'reservas'
		ordering = ('-booking_date',)
		verbose_name = 'Reserva'
		verbose_name_plural = 'Reservas'

	def __str__(self):
		return f"Booking {self.booking_number} ({self.customer.email})"


class Passenger(models.Model):
	TYPE_ADULT = 'adult'
	TYPE_CHILD = 'child'
	TYPE_INFANT = 'infant'

	PASSENGER_TYPE_CHOICES = [
		(TYPE_ADULT, 'Adulto'),
		(TYPE_CHILD, 'Niño'),
		(TYPE_INFANT, 'Infante'),
	]

	booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='passengers', verbose_name='Reserva')
	passenger_type = models.CharField(max_length=8, choices=PASSENGER_TYPE_CHOICES, default=TYPE_ADULT, verbose_name='Tipo de pasajero')
	title = models.CharField(max_length=16, null=True, blank=True, verbose_name='Título')
	first_name = models.CharField(max_length=150, verbose_name='Nombre')
	last_name = models.CharField(max_length=150, verbose_name='Apellido')
	date_of_birth = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
	gender = models.CharField(max_length=16, null=True, blank=True, verbose_name='Género')
	passport_number = models.CharField(max_length=64, null=True, blank=True, verbose_name='Número de pasaporte')
	nationality = models.CharField(max_length=64, null=True, blank=True, verbose_name='Nacionalidad')

	class Meta:
		db_table = 'pasajeros_reserva'
		verbose_name = 'Pasajero'
		verbose_name_plural = 'Pasajeros'

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.passenger_type})"


class HotelBooking(models.Model):
	booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='hotel_bookings', verbose_name='Reserva')
	hotel = models.ForeignKey('hotels.Hotel', on_delete=models.SET_NULL, null=True, blank=True, related_name='hotel_reservations', verbose_name='Hotel')
	check_in_date = models.DateField(verbose_name='Fecha de entrada')
	check_out_date = models.DateField(verbose_name='Fecha de salida')
	num_rooms = models.PositiveIntegerField(default=1, verbose_name='Número de habitaciones')
	room_type = models.CharField(max_length=64, null=True, blank=True, verbose_name='Tipo de habitación')
	price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio por noche')
	total_nights = models.PositiveIntegerField(default=1, verbose_name='Total de noches')
	total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio total')
	confirmation_number = models.CharField(max_length=128, null=True, blank=True, verbose_name='Número de confirmación')

	class Meta:
		db_table = 'reservas_hotel'
		verbose_name = 'Reserva de hotel'
		verbose_name_plural = 'Reservas de hotel'

	def __str__(self):
		return f"HotelBooking {self.confirmation_number or self.id} for {self.booking}"


class FlightBooking(models.Model):
	TYPE_OUTBOUND = 'outbound'
	TYPE_RETURN = 'return'

	BOOKING_TYPE_CHOICES = [
		(TYPE_OUTBOUND, 'Ida'),
		(TYPE_RETURN, 'Regreso'),
	]

	booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='flight_bookings', verbose_name='Reserva')
	flight = models.ForeignKey('flights.Flight', on_delete=models.SET_NULL, null=True, blank=True, related_name='flight_reservations', verbose_name='Vuelo')
	booking_type = models.CharField(max_length=8, choices=BOOKING_TYPE_CHOICES, default=TYPE_OUTBOUND, verbose_name='Tipo de vuelo')
	num_passengers = models.PositiveIntegerField(default=1, verbose_name='Número de pasajeros')
	seat_numbers = models.TextField(null=True, blank=True, verbose_name='Números de asiento')
	price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio por persona')
	total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), verbose_name='Precio total')
	pnr_number = models.CharField(max_length=128, null=True, blank=True, verbose_name='Número PNR')

	class Meta:
		db_table = 'reservas_vuelo'
		verbose_name = 'Reserva de vuelo'
		verbose_name_plural = 'Reservas de vuelo'

	def __str__(self):
		return f"FlightBooking {self.pnr_number or self.id} ({self.booking})"
