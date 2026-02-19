from django.contrib import admin
from .models import EmailTemplateContentType, SMSTemplate, EmailNotification, SMSNotification, NotificationPreference


@admin.register(EmailTemplateContentType)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_type', 'subject', 'is_active')
    list_filter = ('template_type', 'is_active')
    search_fields = ('subject', 'body')


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ('template_type', 'message', 'is_active')
    list_filter = ('template_type', 'is_active')
    search_fields = ('message',)


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'email_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('email_address', 'recipient__username')
    readonly_fields = ('created_at',)


@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('phone_number', 'recipient__username')
    readonly_fields = ('created_at',)


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
