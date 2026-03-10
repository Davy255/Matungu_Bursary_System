from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import random
import string
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PasswordResetRequestForm, PasswordResetConfirmForm
from .models import UserProfile, PasswordReset, User

def home(request):
    """Homepage view for the bursary system"""
    return render(request, 'home.html')

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'users:dashboard')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:home')

@login_required
def dashboard(request):
    """User dashboard"""
    has_profile = hasattr(request.user, 'profile')
    applications = request.user.applications.all()[:5]
    return render(request, 'users/dashboard.html', {
        'has_profile': has_profile,
        'applications': applications
    })

@login_required
def profile(request):
    """User profile view"""
    try:
        user_profile = request.user.profile
        creating = False
    except UserProfile.DoesNotExist:
        user_profile = None
        creating = True
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('users:dashboard')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'users/profile.html', {'form': form, 'creating': creating})


def password_reset_request(request):
    """Request password reset"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generate 6-digit code
                code = ''.join(random.choices(string.digits, k=6))
                
                # Delete old unused tokens for this user
                PasswordReset.objects.filter(user=user, is_used=False).delete()
                
                # Create new reset token
                expires_at = timezone.now() + timedelta(hours=1)
                PasswordReset.objects.create(
                    user=user,
                    token=code,
                    expires_at=expires_at
                )
                
                # Send email
                subject = 'Password Reset Code - Bursary Portal'
                message = f'''
Hello {user.first_name or user.username},

You requested to reset your password for the Bursary Management System.

Your verification code is: {code}

This code will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
Bursary Portal Team
                '''
                
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Password reset code has been sent to your email.')
                    request.session['reset_email'] = email
                    return redirect('users:password_reset_confirm')
                except Exception as e:
                    messages.error(request, f'Error sending email. Code: {code} (For development only)')
                    request.session['reset_email'] = email
                    return redirect('users:password_reset_confirm')
                    
            except User.DoesNotExist:
                messages.error(request, 'No account found with that email address.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'users/password_reset_request.html', {'form': form})


def password_reset_confirm(request):
    """Confirm password reset with code"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Please request a password reset first.')
        return redirect('users:password_reset_request')
    
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                reset_token = PasswordReset.objects.get(
                    user=user,
                    token=code,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )
                
                # Update password
                user.set_password(new_password)
                user.save()
                
                # Mark token as used
                reset_token.is_used = True
                reset_token.save()
                
                # Clear session
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                
                messages.success(request, 'Password reset successful! You can now login with your new password.')
                return redirect('users:login')
                
            except PasswordReset.DoesNotExist:
                messages.error(request, 'Invalid or expired reset code.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
    else:
        form = PasswordResetConfirmForm()
    
    return render(request, 'users/password_reset_confirm.html', {'form': form, 'email': email})
