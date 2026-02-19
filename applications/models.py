from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from schools.models import School, Program, Campus
import uuid


class Ward(models.Model):
    """Wards/Constituencies for applicant location tracking"""
    name = models.CharField(max_length=100, unique=True)
    constituency = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['county', 'constituency', 'name']
        indexes = [
            models.Index(fields=['county', 'constituency']),
        ]
    
    def __str__(self):
        if self.constituency:
            return f"{self.name} ({self.constituency}, {self.county})"
        return self.name


class Application(models.Model):
    """Main bursary application model"""
    STATUS_CHOICES = (
        ('Draft', 'Draft - Not Submitted'),
        ('Submitted', 'Submitted - Under Review'),
        ('Under_Review', 'Under Review - Admin Reviewing'),
        ('Needs_Clarification', 'Needs Clarification'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Appeal', 'Under Appeal Review'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    school = models.ForeignKey(School, on_delete=models.PROTECT, related_name='applications')
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='applications')
    ward = models.ForeignKey('Ward', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications', help_text='Applicant\'s ward/constituency')
    
    # Application Details
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft')
    application_date = models.DateTimeField(auto_now_add=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    
    # Personal Information
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[('Single', 'Single'), ('Married', 'Married'), ('Other', 'Other')],
        default='Single'
    )
    
    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Financial Information
    family_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text='Annual family income in KES')
    income_source = models.CharField(max_length=255, blank=True)
    number_of_dependents = models.IntegerField(default=0, blank=True, null=True)
    other_siblings_in_school = models.IntegerField(default=0, blank=True, null=True)
    
    # Academic Information
    course_name = models.CharField(max_length=255, blank=True, help_text='Course/Program you are studying')
    program_level = models.CharField(
        max_length=50,
        choices=[
            ('Certificate', 'Certificate'),
            ('Diploma', 'Diploma'),
            ('Higher Diploma', 'Higher Diploma'),
            ('Degree', 'Degree (Bachelor)'),
            ('Masters', 'Masters'),
            ('PhD', 'PhD/Doctorate'),
        ],
        blank=True,
        help_text='Level of study program'
    )
    year_of_study = models.CharField(
        max_length=20,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year'),
            ('6th Year', '6th Year'),
        ],
        blank=True,
        help_text='Current year of study'
    )
    is_orphan = models.BooleanField(default=False, help_text='Check if you are an orphan')
    
    # Application Essay/Statement
    motivation_letter = models.TextField(blank=True, help_text='Why you need this bursary')
    expected_challenges = models.TextField(blank=True, help_text='Financial challenges you face')
    
    # Tracking
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_date = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['applicant', 'status']),
            models.Index(fields=['school', 'status']),
            models.Index(fields=['status', 'submitted_date']),
        ]
        permissions = (
            ('can_approve_applications', 'Can approve applications'),
            ('can_reject_applications', 'Can reject applications'),
            ('can_comment_applications', 'Can comment on applications'),
            ('can_review_applications', 'Can review applications'),
        )
    
    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.school.name} ({self.status})"


class ApplicationDocument(models.Model):
    """Documents required for application"""
    DOCUMENT_TYPES = (
        ('Admission_Letter', 'Admission Letter'),
        ('Birth_Certificate', 'Birth Certificate'),
        ('National_ID', 'National ID'),
        ('Fee_Structure', 'School Fee Structure'),
        ('Parents_ID', "Parent's ID"),
        ('Death_Certificate', 'Death Certificate (For Orphans)'),
        ('Other', 'Other Document'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to='applications/documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'])],
        help_text='Max file size: 5MB'
    )
    uploaded_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_documents')
    verified_date = models.DateTimeField(blank=True, null=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['document_type', '-uploaded_date']
        unique_together = ('application', 'document_type')
    
    def __str__(self):
        return f"{self.application.applicant.get_full_name()} - {self.get_document_type_display()}"


class ApplicationReview(models.Model):
    """Admin review and comments on applications"""
    REVIEW_STATUS = (
        ('Pending', 'Pending Review'),
        ('In_Progress', 'In Progress'),
        ('Completed', 'Review Completed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reviews')
    
    # Review Fields
    academic_score = models.IntegerField(default=0, help_text='Score out of 100')
    financial_need_score = models.IntegerField(default=0, help_text='Score out of 100')
    supporting_documents_score = models.IntegerField(default=0, help_text='Score out of 100')
    overall_score = models.IntegerField(default=0, help_text='Final score out of 100')
    
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='Pending')
    recommendation = models.CharField(
        max_length=20,
        choices=[('Approve', 'Approve'), ('Reject', 'Reject'), ('Clarify', 'Needs Clarification')],
        blank=True
    )
    
    comments = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text='For admin use only')
    
    reviewed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reviewed_at']
    
    def __str__(self):
        return f"Review of {self.application.applicant.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Calculate overall score as average
        scores = [self.academic_score, self.financial_need_score, self.supporting_documents_score]
        if any(scores):
            self.overall_score = sum(scores) // len([s for s in scores if s > 0]) if any(scores) else 0
        super().save(*args, **kwargs)


class ApplicationComment(models.Model):
    """Comments from admins on applications"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='application_comments')
    comment = models.TextField()
    is_internal = models.BooleanField(default=False, help_text='Internal comment not visible to applicant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.commented_by.get_full_name()} on {self.application.applicant.get_full_name()}'s application"


class ApplicationApproval(models.Model):
    """Track approval decisions"""
    APPROVAL_LEVELS = (
        ('Ward_Admin', 'Ward Admin'),
        ('CDF_Admin', 'CDF Admin'),
        ('Super_Admin', 'Super Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='approvals')
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals_given')
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS)
    status = models.CharField(
        max_length=20,
        choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')]
    )
    reason = models.TextField(blank=True)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Approved amount in KES')
    approved_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-approved_date']
    
    def __str__(self):
        return f"{self.application.applicant.get_full_name()} - {self.approval_level}: {self.status}"
