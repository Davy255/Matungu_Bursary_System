from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, AdminRole
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


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
