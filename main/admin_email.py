from django.core.mail import EmailMessage
from django.conf import settings

def send_admin_notification(subject: str, body: str, to: list[str], from_email: str = None) -> None:
    """
    Sends an email using the *admin* SMTP backend.
    Used for administrative actions to avoid interfering with security-related integrations.
    """
    # Obtain a connection that points to the ADMIN_EMAIL_* settings
    connection = settings.get_admin_email_connection()

    # Use the admin email as sender if not provided
    sender = from_email or settings.ADMIN_EMAIL_HOST_USER or settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
        subject   = subject,
        body      = body,
        from_email= sender,
        to        = to,
        connection= connection,
    )
    email.send(fail_silently=False)
