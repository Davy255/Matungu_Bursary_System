from django.db import models
from django.contrib.auth.models import User
from applications.models import Application
import uuid


class EmailTemplateContentType(models.Model):
    """Templates for email notifications"""
    TEMPLATE_TYPES = (
        ('application_submitted', 'Application Submitted'),
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('application_needs_clarification', 'Application Needs Clarification'),
        ('new_comment', 'New Comment on Your Application'),
        ('status_update', 'Status Update'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text='Use {{var_name}} for variables')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Email Templates'
    
    def __str__(self):
        return f"{self.get_template_type_display()} Template"


class SMSTemplate(models.Model):
    """Templates for SMS notifications"""
    TEMPLATE_TYPES = (
        ('application_submitted', 'Application Submitted'),
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('status_update', 'Status Update'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES, unique=True)
    message = models.CharField(max_length=160, help_text='SMS character limit: 160')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_template_type_display()} SMS"


class EmailNotification(models.Model):
    """Track email notifications"""
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Bounced', 'Bounced'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_notifications')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='email_notifications')
    email_address = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notification_type = models.CharField(max_length=50, blank=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Email to {self.email_address} - {self.status}"


class SMSNotification(models.Model):
    """Track SMS notifications"""
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
        ('Delivered', 'Delivered'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_notifications')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='sms_notifications')
    phone_number = models.CharField(max_length=20)
    message = models.CharField(max_length=160)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notification_type = models.CharField(max_length=50, blank=True)
    sent_date = models.DateTimeField(blank=True, null=True)
    twilio_message_id = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SMS to {self.phone_number} - {self.status}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preference')
    email_on_submission = models.BooleanField(default=True)
    email_on_approval = models.BooleanField(default=True)
    email_on_rejection = models.BooleanField(default=True)
    email_on_comment= models.BooleanField(default=True)
    email_on_update = models.BooleanField(default=True)
    
    sms_on_submission = models.BooleanField(default=False)
    sms_on_approval = models.BooleanField(default=True)
    sms_on_rejection = models.BooleanField(default=True)
    sms_on_update = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.get_full_name()}"
