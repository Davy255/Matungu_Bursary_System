from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, AdminRoleAssignmentForm
from .models import UserProfile, AdminRole, Notification
from applications.models import Application


@require_http_methods(["GET", "POST"])
def register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('users:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('applications:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
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
            ward = form.cleaned_data['ward']
            
            # Check if role already exists
            if AdminRole.objects.filter(user=user, role_type=role_type, ward=ward).exists():
                messages.error(request, 'This user already has this role in the selected ward.')
            else:
                admin_role = form.save(commit=False)
                admin_role.assigned_by = request.user
                admin_role.save()
                
                # Update user profile
                user.profile.user_type = role_type
                user.profile.ward = ward
                user.profile.save()
                
                # Make user staff
                user.is_staff = True
                user.save()
                
                messages.success(request, f'Admin role assigned to {user.get_full_name()}.')
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
