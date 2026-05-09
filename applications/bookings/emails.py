from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# ── Colores de marca ──────────────────────────────────────────────────────────
_WINE   = '#9b1c3a'
_ROSE   = '#c42c54'
_DARK   = '#0f1117'
_CARD   = '#1a1d2e'
_SILVER = '#94a3b8'


def _base_html(title: str, preview: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#0f1117;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <!-- preview text -->
  <span style="display:none;max-height:0;overflow:hidden;color:#0f1117;">{preview}</span>

  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- Logo / header -->
          <tr>
            <td align="center" style="padding:0 0 28px 0;">
              <table cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:{_WINE};border-radius:12px;width:44px;height:44px;text-align:center;vertical-align:middle;">
                    <span style="font-size:22px;line-height:44px;">✈</span>
                  </td>
                  <td style="padding-left:12px;vertical-align:middle;">
                    <span style="font-size:22px;font-weight:800;color:#ffffff;letter-spacing:-0.5px;">
                      Travel<span style="color:{_ROSE};">Agency</span>
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Card -->
          <tr>
            <td style="background:#1a1d2e;border-radius:20px;border:1px solid #2a2d3e;overflow:hidden;">
              {body}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td align="center" style="padding:28px 0 0 0;">
              <p style="margin:0;color:#4a5068;font-size:12px;line-height:1.6;">
                © 2026 TravelAgency · Todos los derechos reservados<br>
                Si no realizaste esta acción, ignora este mensaje.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _row(label: str, value: str, accent: bool = False) -> str:
    color = '#ffffff' if accent else '#cbd5e1'
    weight = '700' if accent else '400'
    return f"""
    <tr>
      <td style="padding:10px 32px;border-bottom:1px solid #2a2d3e;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="color:#64748b;font-size:13px;">{label}</td>
            <td align="right" style="color:{color};font-size:13px;font-weight:{weight};">{value}</td>
          </tr>
        </table>
      </td>
    </tr>"""


def _send(subject: str, to_email: str, html: str, plain: str) -> None:
    msg = EmailMultiAlternatives(
        subject=subject,
        body=plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    msg.attach_alternative(html, 'text/html')
    try:
        msg.send()
    except Exception:
        pass


# ── Confirmación de reserva ───────────────────────────────────────────────────

def send_booking_confirmation(booking):
    customer = booking.customer
    if not customer.email:
        return

    name         = customer.first_name or customer.username
    package_name = booking.package.name if booking.package else 'Reserva personalizada'
    travel_date  = booking.travel_date.strftime('%d/%m/%Y') if booking.travel_date else '—'
    passengers   = f"{booking.num_adults} adulto(s)"
    if booking.num_children:
        passengers += f", {booking.num_children} niño(s)"

    body = f"""
      <!-- Hero -->
      <div style="background:linear-gradient(135deg,{_WINE}22,{_CARD});padding:36px 32px 28px;border-bottom:1px solid #2a2d3e;">
        <p style="margin:0 0 8px;font-size:13px;color:{_ROSE};font-weight:600;letter-spacing:1px;text-transform:uppercase;">Reserva recibida</p>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:800;color:#ffffff;">¡Hola, {name}!</h1>
        <p style="margin:0;font-size:15px;color:#94a3b8;line-height:1.6;">Tu reserva ha sido registrada exitosamente.<br>Pronto recibirás más detalles.</p>
      </div>

      <!-- Badge N° reserva -->
      <div style="padding:20px 32px;border-bottom:1px solid #2a2d3e;background:#12151f;">
        <p style="margin:0;font-size:11px;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;">Número de reserva</p>
        <p style="margin:4px 0 0;font-size:22px;font-weight:800;color:#ffffff;font-family:monospace;letter-spacing:2px;">#{booking.booking_number}</p>
      </div>

      <!-- Detalles -->
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
        {_row('Paquete', package_name)}
        {_row('Fecha de salida', travel_date)}
        {_row('Pasajeros', passengers)}
        {_row('Total', f'USD {booking.total_amount}', accent=True)}
        {_row('Estado de pago', booking.get_payment_status_display())}
      </table>

      <!-- CTA -->
      <div style="padding:28px 32px;text-align:center;">
        <p style="margin:0 0 20px;font-size:14px;color:#94a3b8;">Puedes ver el detalle completo en tu cuenta.</p>
        <p style="margin:0;font-size:14px;color:#64748b;">¡Gracias por elegirnos! 🌍</p>
      </div>
    """

    plain = f"Hola {name},\n\nTu reserva #{booking.booking_number} fue registrada.\nPaquete: {package_name}\nSalida: {travel_date}\nTotal: USD {booking.total_amount}\n\nTravelAgency"

    _send(f'✈ Confirmación de reserva #{booking.booking_number}', customer.email, _base_html('Reserva confirmada', f'Tu reserva #{booking.booking_number} fue registrada', body), plain)


# ── Confirmación de pago ──────────────────────────────────────────────────────

def send_payment_confirmation(booking):
    customer = booking.customer
    if not customer.email:
        return

    name         = customer.first_name or customer.username
    package_name = booking.package.name if booking.package else 'Reserva personalizada'

    body = f"""
      <!-- Hero -->
      <div style="background:linear-gradient(135deg,#0d4f2822,{_CARD});padding:36px 32px 28px;border-bottom:1px solid #2a2d3e;">
        <p style="margin:0 0 8px;font-size:13px;color:#34d399;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Pago confirmado</p>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:800;color:#ffffff;">¡Pago exitoso, {name}!</h1>
        <p style="margin:0;font-size:15px;color:#94a3b8;line-height:1.6;">Tu pago fue procesado correctamente.<br>Tu aventura está confirmada. 🎉</p>
      </div>

      <!-- Monto destacado -->
      <div style="padding:24px 32px;border-bottom:1px solid #2a2d3e;background:#12151f;text-align:center;">
        <p style="margin:0;font-size:12px;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;">Monto pagado</p>
        <p style="margin:8px 0 0;font-size:42px;font-weight:900;color:#ffffff;letter-spacing:-1px;">USD {booking.paid_amount}</p>
        <span style="display:inline-block;margin-top:8px;background:#0d4f28;color:#34d399;font-size:12px;font-weight:700;padding:4px 12px;border-radius:20px;letter-spacing:0.5px;">✓ CONFIRMADA</span>
      </div>

      <!-- Detalles -->
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
        {_row('Número de reserva', f'#{booking.booking_number}')}
        {_row('Paquete', package_name, accent=True)}
        {_row('Estado', 'Confirmada ✓')}
      </table>

      <!-- Mensaje final -->
      <div style="padding:28px 32px;text-align:center;">
        <p style="margin:0 0 6px;font-size:16px;font-weight:700;color:#ffffff;">¡Prepárate para tu aventura!</p>
        <p style="margin:0;font-size:14px;color:#64748b;">Lleva este correo como comprobante de tu reserva.</p>
      </div>
    """

    plain = f"Hola {name},\n\nTu pago de USD {booking.paid_amount} fue procesado.\nReserva #{booking.booking_number} — {package_name}\n\nTravelAgency"

    _send(f'💳 Pago confirmado — Reserva #{booking.booking_number}', customer.email, _base_html('Pago confirmado', f'Tu pago de USD {booking.paid_amount} fue procesado', body), plain)


# ── Cancelación ───────────────────────────────────────────────────────────────

def send_booking_cancellation(booking):
    customer = booking.customer
    if not customer.email:
        return

    name         = customer.first_name or customer.username
    package_name = booking.package.name if booking.package else 'Reserva personalizada'

    body = f"""
      <!-- Hero -->
      <div style="background:linear-gradient(135deg,#4f0d0d22,{_CARD});padding:36px 32px 28px;border-bottom:1px solid #2a2d3e;">
        <p style="margin:0 0 8px;font-size:13px;color:#f87171;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Reserva cancelada</p>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:800;color:#ffffff;">Hola, {name}</h1>
        <p style="margin:0;font-size:15px;color:#94a3b8;line-height:1.6;">Tu reserva ha sido cancelada.<br>Esperamos verte pronto en otra ocasión.</p>
      </div>

      <!-- Detalles -->
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
        {_row('Número de reserva', f'#{booking.booking_number}')}
        {_row('Paquete cancelado', package_name, accent=True)}
        {_row('Estado', 'Cancelada')}
      </table>

      <!-- Mensaje final -->
      <div style="padding:28px 32px;text-align:center;">
        <p style="margin:0 0 6px;font-size:14px;color:#94a3b8;">Si tienes alguna duda, contáctanos.</p>
        <p style="margin:0;font-size:14px;color:#64748b;">TravelAgency — siempre a tu disposición.</p>
      </div>
    """

    plain = f"Hola {name},\n\nTu reserva #{booking.booking_number} ({package_name}) ha sido cancelada.\n\nTravelAgency"

    _send(f'❌ Reserva cancelada #{booking.booking_number}', customer.email, _base_html('Reserva cancelada', f'Tu reserva #{booking.booking_number} fue cancelada', body), plain)
