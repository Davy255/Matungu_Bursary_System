from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

# Create your models here.

COUNTY_CHOICES = (
    ('Kakamega', 'Kakamega'),
    ('Trans Nzoia', 'Trans Nzoia'),
    ('Bungoma', 'Bungoma'),
)

WARD_CHOICES = (
    ('Mayoni', 'Mayoni'),
    ('Kholera', 'Kholera'),
    ('Khalaba', 'Khalaba'),
    ('Koyonzo', 'Koyonzo'),
    ('Namamali', 'Namamali'),
)

USER_TYPE_CHOICES = (
    ('Applicant', 'Applicant'),
    ('Ward_Admin', 'Ward Admin'),
    ('CDF_Admin', 'CDF Admin'),
    ('Super_Admin', 'Super Admin'),
)

class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^(\+254|0)[0-9]{9}$', 'Enter a valid Kenyan phone number')],
        blank=True
    )
    national_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,  # Ensure one person cannot register multiple accounts with same national ID
        help_text="National ID number - must be unique to prevent duplicate accounts"
    )
    county = models.CharField(max_length=50, choices=COUNTY_CHOICES, default='Kakamega')
    ward = models.CharField(max_length=50, choices=WARD_CHOICES, default='Matungu')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Applicant')
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False, help_text="Profile verified by admin")
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_users')
    verification_date = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user_type})"


class AdminRole(models.Model):
    """Model to assign admin roles to users at ward or CDF level"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_role')
    role_type = models.CharField(
        max_length=20,
        choices=[('Ward_Admin', 'Ward Admin'), ('CDF_Admin', 'CDF Admin')],
        help_text="Select the level of administration"
    )
    ward = models.CharField(
        max_length=50, 
        choices=WARD_CHOICES, 
        blank=True, 
        null=True,
        help_text="Required for Ward Admin only. Leave blank for CDF Admin."
    )
    assigned_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigned_admin_roles')
    assigned_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text="Verified by Super Admin")
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_admins')
    verified_date = models.DateTimeField(null=True, blank=True)
    permissions = models.JSONField(default=list, help_text="List of specific permissions")
    
    class Meta:
        ordering = ['-assigned_date']
        # Enforce one admin per person - each user can only have one admin role
        constraints = [
            models.UniqueConstraint(fields=['user'], name='one_admin_per_user')
        ]
    
    def __str__(self):
        ward_display = f" ({self.ward})" if self.ward else ""
        return f"{self.user.get_full_name()} - {self.role_type}{ward_display}"


class Notification(models.Model):
    """Model for system notifications"""
    NOTIFICATION_TYPES = (
        ('Application_Submitted', 'Application Submitted'),
        ('Application_Approved', 'Application Approved'),
        ('Application_Rejected', 'Application Rejected'),
        ('Review_Added', 'Review Added'),
        ('Status_Update', 'Status Update'),
        ('System_Message', 'System Message'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
