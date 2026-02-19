from django.contrib import admin
from .models import SchoolCategory, School, Campus, Program


@admin.register(SchoolCategory)
class SchoolCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'location', 'code', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'code')
        }),
        ('Location', {
            'fields': ('county', 'location')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Details', {
            'fields': ('description', 'logo', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'location', 'is_main_campus', 'is_active')
    list_filter = ('school', 'is_main_campus', 'is_active')
    search_fields = ('name', 'location', 'city')
    readonly_fields = ('created_at',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'level', 'duration_months', 'tuition_fee', 'is_active')
    list_filter = ('level', 'school', 'is_active')
    search_fields = ('name', 'school__name')
    fieldsets = (
        ('Basic Information', {
            'fields': ('school', 'name', 'level')
        }),
        ('Details', {
            'fields': ('duration_months', 'tuition_fee', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
