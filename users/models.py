from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Administrator'),
        ('reviewer', 'Reviewer'),
    ]
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class UserProfile(models.Model):
    """Extended user profile information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    county = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    ward = models.ForeignKey('applications.Ward', on_delete=models.SET_NULL, null=True)
    guardian_name = models.CharField(max_length=200)
    guardian_phone = models.CharField(max_length=15)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class AdminRole(models.Model):
    """Admin-specific roles and permissions"""
    ROLE_TYPES = [
        ('super_admin', 'Super Administrator'),
        ('reviewer', 'Application Reviewer'),
        ('finance', 'Finance Officer'),
        ('support', 'Support Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_role')
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES)
    department = models.CharField(max_length=100)
    can_approve = models.BooleanField(default=False)
    can_review = models.BooleanField(default=True)
    can_manage_schools = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_type_display()}"


class PasswordReset(models.Model):
    """Password reset tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset token for {self.user.username}"

    class Meta:
        ordering = ['-created_at']
