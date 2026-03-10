from django.contrib import admin
from .models import School, Campus, Program

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
	list_display = ['name', 'school_type', 'registration_number', 'county', 'is_active']
	list_filter = ['school_type', 'is_active', 'county']
	search_fields = ['name', 'registration_number', 'email']

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
	list_display = ['school', 'name', 'location', 'is_main']
	list_filter = ['school', 'is_main']
	search_fields = ['name', 'location', 'school__name']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
	list_display = ['name', 'code', 'school', 'level', 'duration_years', 'is_active']
	list_filter = ['level', 'is_active', 'school']
	search_fields = ['name', 'code', 'school__name']
