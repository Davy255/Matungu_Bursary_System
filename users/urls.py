from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password-reset/new/', views.password_reset_set, name='password_reset_set'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.user_notifications, name='notifications'),
    path('notifications/<str:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Admin role management
    path('assign-admin-role/', views.assign_admin_role, name='assign_admin_role'),
    path('admins/', views.list_admins, name='list_admins'),
    path('admins/<str:admin_id>/deactivate/', views.deactivate_admin, name='deactivate_admin'),
    
    # Verification management (Super Admin only)
    path('manage-verifications/', views.manage_verifications, name='manage_verifications'),
    path('verify-admin/<str:admin_id>/', views.verify_admin, name='verify_admin'),
    path('verify-user/<int:user_id>/', views.verify_user, name='verify_user'),
    path('unverify-admin/<str:admin_id>/', views.unverify_admin, name='unverify_admin'),
    path('unverify-user/<int:user_id>/', views.unverify_user, name='unverify_user'),
]
