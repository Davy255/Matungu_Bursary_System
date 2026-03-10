from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, AdminRole, PasswordReset

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	list_display = ['username', 'email', 'role', 'is_verified', 'date_joined']
	list_filter = ['role', 'is_verified', 'is_staff']
	search_fields = ['username', 'email', 'first_name', 'last_name']
	fieldsets = BaseUserAdmin.fieldsets + (
		('Custom Fields', {'fields': ('role', 'phone_number', 'is_verified')}),
	)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'id_number', 'gender', 'county', 'ward']
	search_fields = ['user__username', 'id_number', 'county']
	list_filter = ['gender', 'county']

@admin.register(AdminRole)
class AdminRoleAdmin(admin.ModelAdmin):
	list_display = ['user', 'role_type', 'department', 'can_approve', 'can_review']
	list_filter = ['role_type', 'can_approve', 'can_review']
	search_fields = ['user__username', 'department']

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
	list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
	list_filter = ['is_used', 'created_at']
	search_fields = ['user__username', 'token']
