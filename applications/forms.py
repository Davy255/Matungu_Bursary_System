from django import forms
from .models import Application, ApplicationDocument
from schools.models import School

SCHOOL_CATEGORY_CHOICES = [
    ('', '-- Select Category --'),
    ('university', 'University'),
    ('college', 'College'),
    ('polytechnic', 'National Polytechnic'),
    ('ttc', 'Teachers Training College (TTC)'),
]

class ApplicationForm(forms.ModelForm):
    """Form for bursary application"""
    school_category = forms.ChoiceField(
        choices=SCHOOL_CATEGORY_CHOICES,
        required=True,
        label='School Category',
    )

    class Meta:
        model = Application
        fields = [
            'school_category',
            'school',
            'course_name',
            'admission_number',
            'year_of_study',
            'family_income',
            'amount_requested',
            'reason',
        ]
        widgets = {
            'school':           forms.Select(attrs={'class': 'form-control', 'id': 'id_school'}),
            'course_name':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bachelor of Science in Computer Science'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ADM/2024/001'}),
            'year_of_study':    forms.Select(attrs={'class': 'form-control'}),
            'family_income':    forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'reason':           forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Explain why you need financial assistance...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Start with empty school list; JS will populate based on chosen category
        self.fields['school'].queryset = School.objects.filter(is_active=True).order_by('name')
        self.fields['school'].empty_label = '-- Select School --'
        self.fields['course_name'].required = True


class ApplicationDocumentForm(forms.ModelForm):
    """Form for document upload"""
    class Meta:
        model = ApplicationDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size cannot exceed 5MB')
        return file

