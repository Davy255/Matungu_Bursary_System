from django.contrib import admin
from .models import Ward, Application, ApplicationDocument, ApplicationReview, ApplicationApproval, BursarySettings

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
	list_display = ['name', 'sub_county', 'county', 'code']
	list_filter = ['county', 'sub_county']
	search_fields = ['name', 'code', 'county']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ['application_number', 'applicant', 'school', 'status', 'amount_requested', 'submitted_at']
	list_filter = ['status', 'school', 'year_of_study']
	search_fields = ['application_number', 'applicant__username', 'admission_number']
	readonly_fields = ['application_number', 'created_at', 'updated_at']

@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
	list_display = ['application', 'document_type', 'file_name', 'uploaded_at']
	list_filter = ['document_type', 'uploaded_at']
	search_fields = ['application__application_number', 'file_name']

@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
	list_display = ['application', 'reviewer', 'score', 'recommendation', 'reviewed_at']
	list_filter = ['recommendation', 'reviewed_at']
	search_fields = ['application__application_number', 'reviewer__username']

@admin.register(ApplicationApproval)
class ApplicationApprovalAdmin(admin.ModelAdmin):
	list_display = ['application', 'approver', 'approved_amount', 'disbursement_date', 'approved_at']
	list_filter = ['approved_at', 'disbursement_date']
	search_fields = ['application__application_number', 'approver__username', 'disbursement_reference']


@admin.register(BursarySettings)
class BursarySettingsAdmin(admin.ModelAdmin):
	"""Singleton admin — only one row ever exists (pk=1)."""
	list_display = ['academic_year', 'application_deadline', 'is_accepting_applications', 'max_amount', 'updated_at']
	fieldsets = (
		('Academic Year', {
			'fields': ('academic_year',),
		}),
		('Application Window', {
			'fields': ('is_accepting_applications', 'application_deadline'),
			'description': 'Set the deadline date/time and toggle whether applications are currently open.',
		}),
		('Limits & Announcements', {
			'fields': ('max_amount', 'announcement'),
		}),
	)

	def has_add_permission(self, request):
		# Allow adding only if no instance exists yet
		return not BursarySettings.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False  # Prevent deletion of the singleton

	def changelist_view(self, request, extra_context=None):
		# Redirect straight to the edit page of the singleton
		obj = BursarySettings.get_settings()
		from django.http import HttpResponseRedirect
		from django.urls import reverse
		return HttpResponseRedirect(
			reverse('admin:applications_bursarysettings_change', args=[obj.pk])
		)
