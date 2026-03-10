from django.db import models
from users.models import User

class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('application_submitted', 'Application Submitted'),
        ('application_reviewed', 'Application Reviewed'),
        ('application_approved', 'Application Approved'),
        ('application_rejected', 'Application Rejected'),
        ('documents_required', 'Documents Required'),
        ('disbursement', 'Disbursement'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
