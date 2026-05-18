from .models import Notification


def notify(user, title, message, type=Notification.TYPE_SYSTEM, link=''):
    Notification.objects.create(user=user, title=title, message=message, type=type, link=link)


def notify_booking_created(booking):
    notify(
        user=booking.customer,
        title='Reserva creada',
        message=f'Tu reserva #{booking.booking_number} fue registrada exitosamente.',
        type=Notification.TYPE_BOOKING,
        link=f'/bookings/{booking.id}',
    )


def notify_payment_confirmed(booking):
    notify(
        user=booking.customer,
        title='Pago confirmado',
        message=f'Tu pago de USD {booking.paid_amount} para la reserva #{booking.booking_number} fue procesado.',
        type=Notification.TYPE_PAYMENT,
        link=f'/bookings/{booking.id}',
    )


def notify_booking_cancelled(booking):
    notify(
        user=booking.customer,
        title='Reserva cancelada',
        message=f'Tu reserva #{booking.booking_number} ha sido cancelada.',
        type=Notification.TYPE_BOOKING,
        link=f'/bookings/{booking.id}',
    )


def notify_booking_confirmed(booking):
    notify(
        user=booking.customer,
        title='Reserva confirmada',
        message=f'Tu reserva #{booking.booking_number} ha sido confirmada. ¡Prepárate para viajar!',
        type=Notification.TYPE_BOOKING,
        link=f'/bookings/{booking.id}',
    )


def notify_booking_completed(booking):
    notify(
        user=booking.customer,
        title='Reserva completada',
        message=f'Tu reserva #{booking.booking_number} ha sido marcada como completada. ¡Gracias por viajar con nosotros!',
        type=Notification.TYPE_BOOKING,
        link=f'/bookings/{booking.id}',
    )
