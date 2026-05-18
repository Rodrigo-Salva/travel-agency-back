from django.core.mail import EmailMultiAlternatives
from django.conf import settings

_WINE   = '#622347'
_ROSE   = '#c42c54'
_DARK   = '#0f1117'
_CARD   = '#1a1d2e'


def _base_html(title: str, preview: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#0f1117;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <span style="display:none;max-height:0;overflow:hidden;color:#0f1117;">{preview}</span>
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f1117;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
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
        <tr>
          <td style="background:#1a1d2e;border-radius:20px;border:1px solid #2a2d3e;overflow:hidden;">
            {body}
          </td>
        </tr>
        <tr>
          <td align="center" style="padding:28px 0 0 0;">
            <p style="margin:0;color:#4a5068;font-size:12px;line-height:1.6;">
              © 2026 TravelAgency · Todos los derechos reservados<br>
              Si no realizaste esta acción, ignora este mensaje.
            </p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


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


def send_password_reset(user, reset_url: str) -> None:
    name = user.first_name or user.username
    body = f"""
      <div style="background:linear-gradient(135deg,{_WINE}22,{_CARD});padding:36px 32px 28px;border-bottom:1px solid #2a2d3e;">
        <p style="margin:0 0 8px;font-size:13px;color:{_ROSE};font-weight:600;letter-spacing:1px;text-transform:uppercase;">Recuperar contraseña</p>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:800;color:#ffffff;">Hola, {name}</h1>
        <p style="margin:0;font-size:15px;color:#94a3b8;line-height:1.6;">Recibimos una solicitud para restablecer tu contraseña.<br>El enlace expira en <strong style="color:#ffffff;">30 minutos</strong>.</p>
      </div>
      <div style="padding:32px;text-align:center;">
        <p style="margin:0 0 24px;font-size:14px;color:#94a3b8;">Haz clic en el botón para crear una nueva contraseña:</p>
        <a href="{reset_url}"
           style="display:inline-block;background:{_WINE};color:#ffffff;font-size:15px;font-weight:700;padding:14px 36px;border-radius:12px;text-decoration:none;letter-spacing:0.3px;">
          Restablecer contraseña
        </a>
        <p style="margin:24px 0 0;font-size:12px;color:#4a5068;">Si el botón no funciona, copia este enlace en tu navegador:<br>
          <span style="color:#94a3b8;word-break:break-all;">{reset_url}</span>
        </p>
      </div>
      <div style="padding:0 32px 24px;border-top:1px solid #2a2d3e;margin-top:8px;">
        <p style="margin:16px 0 0;font-size:12px;color:#4a5068;">Si no solicitaste este cambio, puedes ignorar este correo. Tu contraseña no será modificada.</p>
      </div>
    """
    plain = (
        f"Hola {name},\n\n"
        f"Recibimos una solicitud para restablecer tu contraseña.\n"
        f"Usa el siguiente enlace (válido 30 minutos):\n\n{reset_url}\n\n"
        f"Si no solicitaste este cambio, ignora este mensaje.\n\nTravelAgency"
    )
    _send('🔑 Restablecer contraseña — TravelAgency', user.email,
          _base_html('Restablecer contraseña', 'Enlace para crear una nueva contraseña', body), plain)


def send_password_changed(user) -> None:
    name = user.first_name or user.username
    body = f"""
      <div style="background:linear-gradient(135deg,#0d4f2822,{_CARD});padding:36px 32px 28px;border-bottom:1px solid #2a2d3e;">
        <p style="margin:0 0 8px;font-size:13px;color:#34d399;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Contraseña actualizada</p>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:800;color:#ffffff;">Hola, {name}</h1>
        <p style="margin:0;font-size:15px;color:#94a3b8;line-height:1.6;">Tu contraseña fue cambiada exitosamente.</p>
      </div>
      <div style="padding:28px 32px;text-align:center;">
        <div style="display:inline-block;background:#0d4f28;color:#34d399;font-size:13px;font-weight:700;padding:8px 20px;border-radius:20px;letter-spacing:0.5px;">✓ CONTRASEÑA ACTUALIZADA</div>
        <p style="margin:20px 0 0;font-size:14px;color:#94a3b8;">Si no realizaste este cambio, contacta a soporte de inmediato.</p>
      </div>
    """
    plain = (
        f"Hola {name},\n\n"
        f"Tu contraseña fue cambiada exitosamente.\n"
        f"Si no realizaste este cambio, contacta a soporte.\n\nTravelAgency"
    )
    _send('🔐 Contraseña actualizada — TravelAgency', user.email,
          _base_html('Contraseña actualizada', 'Tu contraseña fue cambiada', body), plain)
