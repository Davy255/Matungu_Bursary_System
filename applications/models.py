from django.db import models
from users.models import User
from schools.models import School, Campus, Program

class Ward(models.Model):
    """Administrative wards"""
    name = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.sub_county}"

    class Meta:
        ordering = ['county', 'sub_county', 'name']


class Application(models.Model):
    """Bursary applications"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    ]
    
    ACADEMIC_YEARS = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year'),
        ('6', 'Sixth Year'),
    ]
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    application_number = models.CharField(max_length=50, unique=True)
    
    # School Information
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True, blank=True)
    course_name = models.CharField(max_length=200, blank=True, help_text="Name of your course/programme")
    admission_number = models.CharField(max_length=50)
    year_of_study = models.CharField(max_length=1, choices=ACADEMIC_YEARS)
    
    # Financial Information
    family_income = models.DecimalField(max_digits=10, decimal_places=2)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Application Details
    reason = models.TextField(help_text="Reason for applying")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.application_number} - {self.applicant.username}"

    class Meta:
        ordering = ['-created_at']


class ApplicationDocument(models.Model):
    """Documents attached to applications"""
    DOCUMENT_TYPES = [
        ('id', 'ID/Birth Certificate'),
        ('admission', 'Admission Letter'),
        ('fee_structure', 'Fee Structure'),
        ('income_proof', 'Income Proof'),
        ('parent_id', 'Parent/Guardian ID'),
        ('other', 'Other'),
    ]
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='applications/documents/%Y/%m/')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.application.application_number}"

    class Meta:
        ordering = ['-uploaded_at']


class ApplicationReview(models.Model):
    """Reviews by administrators"""
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.IntegerField(help_text="Score out of 100")
    comments = models.TextField()
    recommendation = models.CharField(
        max_length=20,
        choices=[
            ('approve', 'Approve'),
            ('reject', 'Reject'),
            ('needs_info', 'Needs More Information'),
        ]
    )
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.application.application_number}"

    class Meta:
        ordering = ['-reviewed_at']


class ApplicationApproval(models.Model):
    """Final approval records"""
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='approval')
    approver = models.ForeignKey(User, on_delete=models.PROTECT)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approval_notes = models.TextField(blank=True)
    disbursement_date = models.DateField(null=True, blank=True)
    disbursement_reference = models.CharField(max_length=100, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Approval for {self.application.application_number}"

    class Meta:
        ordering = ['-approved_at']
