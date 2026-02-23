from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import secrets
import time
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, AdminRoleAssignmentForm
from .models import UserProfile, AdminRole, Notification
from applications.models import Application, RegistrationSettings

PASSWORD_RESET_CODE_TTL = 600  # 10 minutes
PASSWORD_RESET_MAX_REQUESTS = 3
PASSWORD_RESET_REQUEST_WINDOW = 600  # 10 minutes
PASSWORD_RESET_RESEND_COOLDOWN = 60  # 1 minute
PASSWORD_RESET_MAX_VERIFY_ATTEMPTS = 5
PASSWORD_RESET_LOCKOUT_TTL = 900  # 15 minutes


def _get_reset_code_key(email):
    return f"password_reset_code:{email.lower().strip()}"


def _get_reset_rate_key(email):
    return f"password_reset_rate:{email.lower().strip()}"


def _get_reset_resend_key(email):
    return f"password_reset_resend:{email.lower().strip()}"


def _get_reset_attempts_key(email):
    return f"password_reset_attempts:{email.lower().strip()}"


def _get_reset_lock_key(email):
    return f"password_reset_lock:{email.lower().strip()}"


def _generate_reset_code():
    return f"{secrets.randbelow(1000000):06d}"


def index_view(request):
    """Index view - redirects based on authentication status"""
    if request.user.is_authenticated:
        # Ensure user has a profile
        UserProfile.objects.get_or_create(user=request.user)
        
        # Redirect admins to admin panel
        if request.user.is_staff or hasattr(request.user, 'admin_role'):
            return redirect('admin_panel:dashboard')
        
        # Redirect regular users to applicant dashboard
        return redirect('applications:dashboard')
    
    return redirect('users:login')


@require_http_methods(["GET", "POST"])
def register(request):
    """Handle user registration with national ID verification"""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')
    
    # Check if registration is open
    try:
        settings = RegistrationSettings.objects.first()
        if settings:
            if not settings.is_registration_open:
                messages.error(request, 'Registration is currently closed. Please contact the CDF office.')
                return redirect('users:login')
            
            # Check if deadline has passed
            if settings.deadline_date and timezone.now() > settings.deadline_date:
                messages.error(request, 'Registration deadline has passed. Registration is now closed.')
                return redirect('users:login')
    except:
        pass  # If settings don't exist, allow registration
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id'].strip()
            
            # Double-check national ID is not already in system (fraud prevention)
            if UserProfile.objects.filter(national_id=national_id, user__is_active=True).exists():
                messages.error(
                    request,
                    'This National ID is already registered. Only one account per person is allowed. '
                    'If this is your account, please log in instead.'
                )
                return render(request, 'users/register.html', {
                    'form': form,
                    'reg_open': True,
                    'deadline_msg': None,
                    'fraud_warning': True
                })
            
            # Create user
            user = form.save()
            
            # Update UserProfile with national ID
            UserProfile.objects.filter(user=user).update(
                national_id=national_id,
                user_type='Applicant'
            )
            
            messages.success(
                request,
                'Registration successful! Your account has been created with your National ID. '
                'Please log in to access your dashboard.'
            )
            return redirect('users:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    # Check registration status for template context
    reg_open = True
    deadline_msg = None
    try:
        settings = RegistrationSettings.objects.first()
        if settings:
            reg_open = settings.is_registration_open
            if settings.deadline_date:
                deadline_msg = f"Registration closes on {settings.deadline_date.strftime('%B %d, %Y at %H:%M')}"
    except:
        pass
    
    return render(request, 'users/register.html', {
        'form': form,
        'reg_open': reg_open,
        'deadline_msg': deadline_msg,
        'fraud_warning': False
    })


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login with mandatory national ID verification for fraud prevention"""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        national_id = (request.POST.get('national_id', '') or '').strip()  # REQUIRED for fraud prevention
        
        # Check if national ID is provided
        if not national_id:
            messages.error(
                request,
                'National ID is required for login. This helps us verify your identity and prevent fraud.'
            )
            return render(request, 'users/login.html')
        
        # Authenticate user with username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Verify National ID matches registered ID (MANDATORY)
            user_national_id = user.profile.national_id if hasattr(user, 'profile') else None
            if not user_national_id or user_national_id != national_id:
                messages.error(
                    request,
                    'National ID does not match the registered ID for this account. Access denied.'
                )
                return render(request, 'users/login.html')
            
            # All verification passed - login user
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')

            # Ensure profile exists before accessing user_type
            UserProfile.objects.get_or_create(user=user)

            # Redirect based on user role
            if user.profile.user_type == 'Applicant':
                return redirect('applications:dashboard')
            else:
                return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')


@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    """Request a password reset code via email."""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')

    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        if not email:
            messages.error(request, 'Email address is required.')
            return render(request, 'users/password_reset_request.html')

        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            messages.error(request, 'No active account found with that email address.')
            return render(request, 'users/password_reset_request.html')

        lock_key = _get_reset_lock_key(email)
        if cache.get(lock_key):
            messages.error(
                request,
                'This account is temporarily locked due to too many failed attempts. '
                'Please try again later.'
            )
            return render(request, 'users/password_reset_request.html')

        rate_key = _get_reset_rate_key(email)
        request_count = cache.get(rate_key, 0)
        if request_count >= PASSWORD_RESET_MAX_REQUESTS:
            messages.error(
                request,
                'Too many reset requests. Please wait a few minutes and try again.'
            )
            return render(request, 'users/password_reset_request.html')

        resend_key = _get_reset_resend_key(email)
        last_sent = cache.get(resend_key)
        if last_sent:
            elapsed = int(time.time() - last_sent)
            remaining = PASSWORD_RESET_RESEND_COOLDOWN - elapsed
            if remaining > 0:
                messages.error(
                    request,
                    f'Please wait {remaining} seconds before requesting a new code.'
                )
                return render(request, 'users/password_reset_request.html', {
                    'resend_seconds': remaining
                })

        code = _generate_reset_code()
        cache.set(_get_reset_code_key(email), code, timeout=PASSWORD_RESET_CODE_TTL)
        request.session['password_reset_email'] = email
        cache.set(rate_key, request_count + 1, timeout=PASSWORD_RESET_REQUEST_WINDOW)
        cache.set(resend_key, time.time(), timeout=PASSWORD_RESET_RESEND_COOLDOWN)

        subject = 'Bursary System Password Reset Code'
        message = (
            f"Your password reset code is: {code}\n\n"
            f"This code expires in {PASSWORD_RESET_CODE_TTL // 60} minutes. "
            "If you did not request this reset, you can ignore this email."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(request, 'A 6-digit code has been sent to your email.')
        return redirect('users:password_reset_verify')

    return render(request, 'users/password_reset_request.html')


@require_http_methods(["GET", "POST"])
def password_reset_verify(request):
    """Verify the emailed password reset code."""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')

    email = request.session.get('password_reset_email')
    if not email:
        messages.error(request, 'Please request a password reset code first.')
        return redirect('users:password_reset')

    if cache.get(_get_reset_lock_key(email)):
        messages.error(
            request,
            'This account is temporarily locked due to too many failed attempts. '
            'Please try again later.'
        )
        return redirect('users:password_reset')

    resend_seconds = 0
    last_sent = cache.get(_get_reset_resend_key(email))
    if last_sent:
        elapsed = int(time.time() - last_sent)
        remaining = PASSWORD_RESET_RESEND_COOLDOWN - elapsed
        if remaining > 0:
            resend_seconds = remaining

    if request.method == 'POST':
        code = (request.POST.get('code') or '').strip()
        if not code:
            messages.error(request, 'Reset code is required.')
            return render(request, 'users/password_reset_verify.html', {
                'email': email,
                'resend_seconds': resend_seconds
            })

        cached_code = cache.get(_get_reset_code_key(email))
        if not cached_code or cached_code != code:
            attempts_key = _get_reset_attempts_key(email)
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, timeout=PASSWORD_RESET_CODE_TTL)

            remaining_attempts = PASSWORD_RESET_MAX_VERIFY_ATTEMPTS - attempts
            if remaining_attempts <= 0:
                cache.set(_get_reset_lock_key(email), True, timeout=PASSWORD_RESET_LOCKOUT_TTL)
                cache.delete(_get_reset_code_key(email))
                messages.error(
                    request,
                    'Too many incorrect attempts. Please wait and request a new code.'
                )
                return redirect('users:password_reset')

            messages.error(
                request,
                f'Invalid or expired reset code. You have {remaining_attempts} attempts remaining.'
            )
            return render(request, 'users/password_reset_verify.html', {
                'email': email,
                'resend_seconds': resend_seconds
            })

        cache.delete(_get_reset_attempts_key(email))
        request.session['password_reset_verified'] = True
        messages.success(request, 'Code verified. You can now set a new password.')
        return redirect('users:password_reset_set')

    return render(request, 'users/password_reset_verify.html', {
        'email': email,
        'resend_seconds': resend_seconds
    })


@require_http_methods(["GET", "POST"])
def password_reset_set(request):
    """Set a new password after code verification."""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')

    email = request.session.get('password_reset_email')
    verified = request.session.get('password_reset_verified')
    if not email or not verified:
        messages.error(request, 'Please verify your reset code first.')
        return redirect('users:password_reset')

    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1') or ''
        new_password2 = request.POST.get('new_password2') or ''

        if new_password1 != new_password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/password_reset_set.html', {'email': email})

        try:
            validate_password(new_password1)
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
            return render(request, 'users/password_reset_set.html', {'email': email})

        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if not user:
            messages.error(request, 'Account not found. Please request a new reset code.')
            return redirect('users:password_reset')

        user.set_password(new_password1)
        user.save()

        cache.delete(_get_reset_code_key(email))
        request.session.pop('password_reset_email', None)
        request.session.pop('password_reset_verified', None)

        return redirect('users:password_reset_complete')

    return render(request, 'users/password_reset_set.html', {'email': email})


@require_http_methods(["GET"])
def password_reset_complete(request):
    """Password reset complete page."""
    return render(request, 'users/password_reset_complete.html')


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """Display user profile"""
    UserProfile.objects.get_or_create(user=request.user)
    profile = request.user.profile
    admin_role = None
    
    if hasattr(request.user, 'admin_role'):
        admin_role = request.user.admin_role
    
    context = {
        'profile': profile,
        'admin_role': admin_role,
        'is_super_admin': request.user.is_superuser,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    UserProfile.objects.get_or_create(user=request.user)
    profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_super_admin': request.user.is_superuser,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def user_notifications(request):
    """View user notifications"""
    notifications = request.user.notifications.all().order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    # Mark all as read if requested
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_all_read':
            notifications.filter(is_read=False).update(is_read=True)
            messages.success(request, 'All notifications marked as read.')
            return redirect('users:notifications')
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'users/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.read_at = __import__('django.utils.timezone', fromlist=['now']).now()
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('users:notifications')


# SUPER ADMIN VIEWS

def is_super_admin(user):
    """Check if user is super admin"""
    return user.is_staff and user.profile.user_type == 'Super_Admin'


@login_required
def assign_admin_role(request):
    """Super admin view to assign admin roles"""
    if not is_super_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    if request.method == 'POST':
        form = AdminRoleAssignmentForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            role_type = form.cleaned_data['role_type']
            ward = form.cleaned_data.get('ward')  # ward can be None for CDF_Admin
            
            # Check if role already exists
            if role_type == 'CDF_Admin':
                # For CDF_Admin, check if user already has this role (ward doesn't matter)
                if AdminRole.objects.filter(user=user, role_type=role_type).exists():
                    messages.error(request, 'This user already has CDF Admin role.')
                    return render(request, 'admin_panel/assign_admin_role.html', {'form': form})
            else:
                # For Ward_Admin, check role + ward combination
                if AdminRole.objects.filter(user=user, role_type=role_type, ward=ward).exists():
                    messages.error(request, 'This user already has this role in the selected ward.')
                    return render(request, 'admin_panel/assign_admin_role.html', {'form': form})
            
            admin_role = form.save(commit=False)
            admin_role.assigned_by = request.user
            admin_role.save()
            
            # Update user profile
            user.profile.user_type = role_type
            if ward:  # Only update ward if one is specified
                user.profile.ward = ward
            user.profile.save()
            
            # Make user staff
            user.is_staff = True
            user.save()
            
            role_display = f'{role_type.replace("_", " ")} ({ward})' if ward else role_type.replace('_', ' ')
            messages.success(request, f'{role_display} role assigned to {user.get_full_name()}.')
            return redirect('admin_panel:manage_admins')
    else:
        form = AdminRoleAssignmentForm()
    
    context = {'form': form}
    return render(request, 'admin_panel/assign_admin_role.html', context)


@login_required
def list_admins(request):
    """List all admins"""
    if not is_super_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    admins = AdminRole.objects.all().select_related('user', 'assigned_by')
    
    context = {'admins': admins}
    return render(request, 'admin_panel/list_admins.html', context)


@login_required
def deactivate_admin(request, admin_id):
    """Deactivate an admin role"""
    if not is_super_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    admin_role = get_object_or_404(AdminRole, id=admin_id)
    admin_role.is_active = False
    admin_role.save()
    
    messages.success(request, f'Admin role deactivated for {admin_role.user.get_full_name()}.')
    return redirect('admin_panel:manage_admins')


@login_required
def manage_verifications(request):
    """Super admin view to manage user and admin verifications"""
    if not is_super_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    # Get unverified admins
    unverified_admins = AdminRole.objects.filter(is_verified=False).select_related('user', 'assigned_by')
    
    # Get unverified user profiles
    unverified_users = UserProfile.objects.filter(is_verified=False).select_related('user')
    
    # Get recently verified
    recently_verified_admins = AdminRole.objects.filter(is_verified=True).select_related('user', 'verified_by').order_by('-verified_date')[:10]
    recently_verified_users = UserProfile.objects.filter(is_verified=True).select_related('user', 'verified_by').order_by('-verification_date')[:10]
    
    context = {
        'unverified_admins': unverified_admins,
        'unverified_users': unverified_users,
        'recently_verified_admins': recently_verified_admins,
        'recently_verified_users': recently_verified_users,
    }
    return render(request, 'admin_panel/manage_verifications.html', context)


@login_required
def verify_admin(request, admin_id):
    """Super admin verifies an admin account"""
    if not is_super_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    admin_role = get_object_or_404(AdminRole, id=admin_id)
    admin_role.is_verified = True
    admin_role.verified_by = request.user
    admin_role.verified_date = timezone.now()
    admin_role.save()
    
    messages.success(request, f'Admin {admin_role.user.get_full_name()} has been verified.')
    return redirect('users:manage_verifications')


@login_required
def verify_user(request, user_id):
    """Super admin verifies a user profile"""
    if not is_super_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    user_profile.is_verified = True
    user_profile.verified_by = request.user
    user_profile.verification_date = timezone.now()
    user_profile.save()
    
    messages.success(request, f'User {user_profile.user.get_full_name()} has been verified.')
    return redirect('users:manage_verifications')


@login_required
def unverify_admin(request, admin_id):
    """Super admin removes verification from an admin"""
    if not is_super_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    admin_role = get_object_or_404(AdminRole, id=admin_id)
    admin_role.is_verified = False
    admin_role.verified_by = None
    admin_role.verified_date = None
    admin_role.save()
    
    messages.success(request, f'Verification removed for admin {admin_role.user.get_full_name()}.')
    return redirect('users:manage_verifications')


@login_required
def unverify_user(request, user_id):
    """Super admin removes verification from a user"""
    if not is_super_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    user_profile.is_verified = False
    user_profile.verified_by = None
    user_profile.verification_date = None
    user_profile.save()
    
    messages.success(request, f'Verification removed for user {user_profile.user.get_full_name()}.')
    return redirect('users:manage_verifications')
