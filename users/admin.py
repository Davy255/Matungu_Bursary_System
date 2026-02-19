from django.contrib import admin
from .models import UserProfile, AdminRole, Notification


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'national_id', 'user_type', 'ward', 'is_verified', 'created_at')
    list_filter = ('user_type', 'ward', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'national_id', 'phone_number')
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_id')
        }),
        ('Personal Details', {
            'fields': ('phone_number', 'national_id', 'profile_photo')
        }),
        ('Location', {
            'fields': ('county', 'ward')
        }),
        ('System Information', {
            'fields': ('user_type', 'is_verified', 'email_verified', 'phone_verified', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('verification_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdminRole)
class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role_type', 'ward', 'assigned_by', 'assigned_date', 'is_active')
    list_filter = ('role_type', 'ward', 'is_active', 'assigned_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('assigned_date',)
    fieldsets = (
        ('Role Assignment', {
            'fields': ('user', 'role_type', 'ward')
        }),
        ('Authorization', {
            'fields': ('assigned_by', 'permissions')
        }),
        ('Status', {
            'fields': ('is_active', 'assigned_date')
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')
    readonly_fields = ('created_at', 'read_at')
    fieldsets = (
        ('Notification', {
            'fields': ('user', 'notification_type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at', 'read_at')
        }),
    )
