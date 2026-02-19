from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.user_notifications, name='notifications'),
    path('notifications/<str:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Admin role management
    path('assign-admin-role/', views.assign_admin_role, name='assign_admin_role'),
    path('admins/', views.list_admins, name='list_admins'),
    path('admins/<str:admin_id>/deactivate/', views.deactivate_admin, name='deactivate_admin'),
]
