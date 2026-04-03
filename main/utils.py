from django.core.mail import send_mail
from django.conf import settings
from .models import AuditLog

def send_security_alert(user, subject, message):
    full_message = f"Hello {user.username},\n\n{message}\n\nIf this wasn't you, please change your password immediately and contact support."
    send_mail(
        f"Security Alert: {subject}",
        full_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )
    # Log the security alert to AuditLog as well
    log = AuditLog(user=user, action="Security Alert Sent")
    log.details = f"Subject: {subject}"
    log.save()
