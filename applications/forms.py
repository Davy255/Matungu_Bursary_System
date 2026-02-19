from django import forms
from .models import Application, ApplicationDocument, ApplicationReview, ApplicationComment
from django.forms import formset_factory, inlineformset_factory


class ApplicationForm(forms.ModelForm):
    """Main application form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = [
            'date_of_birth',
            'gender',
            'national_id',
            'phone_number',
            'email',
            'family_income',
        ]
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True

    class Meta:
        model = Application
        fields = [
            'ward', 'date_of_birth', 'gender', 'national_id', 'marital_status',
            'phone_number', 'email',
            'family_income', 'income_source', 'number_of_dependents', 'other_siblings_in_school',
            'course_name', 'program_level', 'year_of_study', 'is_orphan',
            'motivation_letter', 'expected_challenges'
        ]
        widgets = {
            'ward': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+254 format'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'family_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'income_source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Farming, Business, Formal Employment'}),
            'number_of_dependents': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_siblings_in_school': forms.NumberInput(attrs={'class': 'form-control'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Bachelor of Science in Computer Science'}),
            'program_level': forms.Select(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'is_orphan': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'motivation_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Explain why you need this bursary...'}),
            'expected_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe financial challenges you face...'}),
        }


class ApplicationDocumentForm(forms.ModelForm):
    """Form for uploading documents"""
    class Meta:
        model = ApplicationDocument
        fields = ['document_type', 'file']
        labels = {
            'document_type': 'Document Type',
            'file': 'Upload File',
        }
        help_texts = {
            'document_type': 'Select the type of document you are uploading',
            'file': 'Accepted formats: PDF, PNG, JPG, DOC, DOCX, XLS, XLSX (Max 5MB)',
        }
        widgets = {
            'document_type': forms.Select(attrs={
                'class': 'form-control',
                'aria-label': 'Document type',
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.png,.jpg,.jpeg,.doc,.docx,.xls,.xlsx',
                'aria-label': 'File upload',
            }),
        }


DocumentFormSet = formset_factory(ApplicationDocumentForm, extra=1, can_delete=True)


class UpdateWardForm(forms.ModelForm):
    """Form for updating ward only"""
    class Meta:
        model = Application
        fields = ['ward']
        widgets = {
            'ward': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }
        labels = {
            'ward': 'Select Your Ward/Constituency',
        }
        help_texts = {
            'ward': 'Choose the ward where you reside',
        }


class SchoolSelectionForm(forms.Form):
    """Form for selecting school, campus, and program"""
    category = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
        label='School Category'
    )
    school = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_school'}),
        label='School'
    )
    campus = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_campus'}),
        label='Campus',
        required=False
    )
    program = forms.CharField(
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_program'}),
        label='Program'
    )


class ApplicationReviewForm(forms.ModelForm):
    """Form for admins to review applications"""
    class Meta:
        model = ApplicationReview
        fields = [
            'academic_score', 'financial_need_score', 'supporting_documents_score',
            'recommendation', 'comments', 'internal_notes'
        ]
        widgets = {
            'academic_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'financial_need_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'supporting_documents_score': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'recommendation': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Comments visible to applicant...'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Internal notes (admin only)...'}),
        }


class ApplicationCommentForm(forms.ModelForm):
    """Form for adding comments to applications"""
    class Meta:
        model = ApplicationComment
        fields = ['comment', 'is_internal']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Add your comment...'}),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ApplicationFilterForm(forms.Form):
    """Form for filtering applications"""
    STATUS_CHOICES = [(choice[0], choice[1]) for choice in Application.STATUS_CHOICES]
    
    status = forms.MultipleChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    school = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filter by school...'}),
        required=False
    )
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )
    search = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search applicant name or ID...'}),
        required=False
    )


class BulkApplicationActionForm(forms.Form):
    """Form for bulk actions on applications"""
    ACTION_CHOICES = [
        ('', '-- Select Action --'),
        ('approve', 'Approve Selected'),
        ('reject', 'Reject Selected'),
        ('export', 'Export Selected'),
    ]
    
    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    application_ids = forms.CharField(widget=forms.HiddenInput())
