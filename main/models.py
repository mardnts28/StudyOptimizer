from django.db import models
from django.contrib.auth.models import User
import pyotp
import hashlib
from django.db.models.signals import pre_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    totp_enabled = models.BooleanField(default=False)

    def generate_totp_secret(self):
        if not self.totp_secret:
            self.totp_secret = pyotp.random_base32()
            self.save()
        return self.totp_secret

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Project', 'Project'),
        ('Research', 'Research'),
        ('Revision', 'Revision'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100, default='General')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['completed', 'due_date']

class SharedMaterial(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Shared Resource', 'Shared Resource'),
        ('Discussion', 'Discussion'),
        ('Revision', 'Review'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_materials')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    content = models.TextField()
    file = models.FileField(upload_to='shared_files/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_materials', blank=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
    emoji = models.CharField(max_length=10, default='📄')


    def __str__(self):
        return self.title

    @property
    def likes_count(self):
        return self.likes.count()

class Comment(models.Model):
    material = models.ForeignKey(SharedMaterial, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.material.title}"

class SummarizedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summaries')
    file_name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default='General')
    subject = models.CharField(max_length=100, default='General')
    summary_text = models.TextField()
    content_hash = models.CharField(max_length=64, blank=True, help_text="SHA-256 integrity hash")
    emoji = models.CharField(max_length=10, default='📄')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class ScheduleItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_items')
    day = models.CharField(max_length=20)
    date = models.DateField(null=True, blank=True)
    time = models.CharField(max_length=50)
    activity = models.CharField(max_length=255)
    color = models.CharField(max_length=20, default='blue')

    def __str__(self):
        return f"{self.day}: {self.activity}"

class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_history')
    password_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

from cryptography.fernet import Fernet
import base64
from django.conf import settings

# Provide a fallback encryption key just in case settings isn't populated
_CIPHER_SUITE = Fernet(base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0')))

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    details_encrypted = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @property
    def details(self):
        try:
            return _CIPHER_SUITE.decrypt(self.details_encrypted.encode('utf-8')).decode('utf-8')
        except:
            return ""
            
    @details.setter
    def details(self, value):
        self.details_encrypted = _CIPHER_SUITE.encrypt(str(value).encode('utf-8')).decode('utf-8')
    
    def __str__(self):
        return f"[{self.timestamp}] {self.user.username if self.user else 'System'}: {self.action}"

class KnownIP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='known_ips')
    ip_address = models.GenericIPAddressField()
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"

# --- Integrity & STRIDE Signals ---

@receiver(pre_save, sender=SummarizedDocument)
def verify_document_integrity(sender, instance, **kwargs):
    """
    STRIDE - Tampering Protection: Ensures the summary text has an integrity hash.
    """
    if not instance.summary_text:
        return
    calc_hash = hashlib.sha256(instance.summary_text.encode('utf-8')).hexdigest()
    if not instance.content_hash:
        instance.content_hash = calc_hash
    elif instance.content_hash != calc_hash:
        instance.content_hash = calc_hash
