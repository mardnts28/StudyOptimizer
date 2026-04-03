from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PasswordHistory, AuditLog
from .utils import send_security_alert

@receiver(post_save, sender=User)
def save_password_history_and_alert(sender, instance, created, **kwargs):
    # Only alert/history if password exists and is not empty (Django's create_user handles this)
    if not instance.password:
        return
        
    last_hist = PasswordHistory.objects.filter(user=instance).order_by('-created_at').first()
    
    # If the hash changed, it means the password was changed
    if not last_hist or last_hist.password_hash != instance.password:
        PasswordHistory.objects.create(user=instance, password_hash=instance.password)
        
        # Don't send "Changed" alert on account CREATION (since it's their first password)
        if not created:
            send_security_alert(
                instance, 
                "Password Changed", 
                "Your account password was recently changed. If this wasn't you, please secure your account immediately."
            )
            log = AuditLog(user=instance, action="Security Alert")
            log.details = "Password Change Notification Sent"
            log.save()
