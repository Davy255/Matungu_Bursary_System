from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, AdminRole
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with national ID validation"""
    email = forms.EmailField(required=True, help_text="Enter a valid email address")
    first_name = forms.CharField(required=True, max_length=30, help_text="Your first name")
    last_name = forms.CharField(required=True, max_length=30, help_text="Your last name")
    national_id = forms.CharField(
        required=True,
        max_length=20,
        help_text="Your National ID number (for fraud prevention - one account per person)"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'national_id', 'password1', 'password2')
    
    def clean_username(self):
        """Validate username is unique"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already in use. Please choose another.')
        return username
    
    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered. Please use a different email or log in.')
        return email

    def clean_national_id(self):
        """Validate national ID is provided and unique"""
        national_id = (self.cleaned_data.get('national_id') or '').strip()
        
        if not national_id:
            raise ValidationError('National ID is required.')
        
        from .models import UserProfile
        
        # Check if national ID already registered
        existing = UserProfile.objects.filter(national_id=national_id, user__is_active=True)
        if existing.exists():
            raise ValidationError(
                'This National ID is already registered in the system. '
                'Only one account per person is allowed. If this is your account, please log in instead.'
            )
        
        return national_id


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'national_id', 'county', 'ward', 'profile_photo']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+254 or 0 format'}),
            'national_id': forms.TextInput(attrs={'placeholder': 'Your National ID'}),
            'county': forms.Select(),
            'ward': forms.Select(),
            'profile_photo': forms.FileInput(),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating basic user info"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AdminRoleAssignmentForm(forms.ModelForm):
    """Form for super admin to assign admin roles"""
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        label='Select User',
        help_text='Only non-staff users are shown'
    )
    
    class Meta:
        model = AdminRole
        fields = ['user', 'role_type', 'ward']
        widgets = {
            'role_type': forms.Select(),
            'ward': forms.Select(),
        }


class AdminPermissionForm(forms.Form):
    """Form for setting specific permissions for admins"""
    PERMISSION_CHOICES = (
        ('view_applications', 'View Applications'),
        ('approve_applications', 'Approve Applications'),
        ('reject_applications', 'Reject Applications'),
        ('add_comments', 'Add Comments to Applications'),
        ('write_reviews', 'Write Reviews'),
        ('view_reports', 'View Reports'),
        ('export_data', 'Export Data'),
        ('manage_users', 'Manage Users in Ward'),
    )
    
    permissions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=PERMISSION_CHOICES,
        help_text='Select permissions for this admin role'
    )
