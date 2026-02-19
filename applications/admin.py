from django.contrib import admin
from .models import Application, ApplicationDocument, ApplicationReview, ApplicationComment, ApplicationApproval, Ward


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'school', 'ward', 'status', 'submitted_date', 'reviewed_by')
    list_filter = ('status', 'school', 'ward__county', 'submitted_date', 'created_at')
    search_fields = ('applicant__username', 'applicant__email', 'national_id', 'ward__name')
    readonly_fields = ('application_date', 'submitted_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Applicant', {
            'fields': ('applicant', 'national_id')
        }),
        ('School & Program', {
            'fields': ('school', 'campus', 'program')
        }),
        ('Location', {
            'fields': ('ward',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'marital_status')
        }),
        ('Contact', {
            'fields': ('phone_number', 'email')
        }),
        ('Financial Information', {
            'fields': ('family_income', 'income_source', 'number_of_dependents', 'other_siblings_in_school')
        }),
        ('Academic Information', {
            'fields': ('course_name', 'program_level', 'year_of_study', 'is_orphan')
        }),
        ('Application', {
            'fields': ('motivation_letter', 'expected_challenges')
        }),
        ('Status & Review', {
            'fields': ('status', 'reviewed_by', 'reviewed_date')
        }),
        ('Timestamps', {
            'fields': ('application_date', 'submitted_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ApplicationDocument)
class ApplicationDocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'uploaded_date', 'is_verified')
    list_filter = ('document_type', 'uploaded_date', 'is_verified')
    search_fields = ('application__applicant__username',)
    readonly_fields = ('uploaded_date',)


@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'reviewer', 'overall_score', 'recommendation', 'reviewed_at')
    list_filter = ('recommendation', 'review_status', 'reviewed_at')
    search_fields = ('application__applicant__username',)
    readonly_fields = ('reviewed_at', 'updated_at')


@admin.register(ApplicationComment)
class ApplicationCommentAdmin(admin.ModelAdmin):
    list_display = ('application', 'commented_by', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('comment', 'application__applicant__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ApplicationApproval)
class ApplicationApprovalAdmin(admin.ModelAdmin):
    list_display = ('application', 'approved_by', 'approval_level', 'status', 'approved_date')
    list_filter = ('approval_level', 'status', 'approved_date')
    search_fields = ('application__applicant__username',)
    readonly_fields = ('approved_date',)


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency', 'county', 'is_active', 'created_at')
    list_filter = ('county', 'is_active', 'created_at')
    search_fields = ('name', 'constituency', 'county')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Ward Information', {
            'fields': ('name', 'constituency', 'county', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
