from django import forms
from .models import Application, ApplicationDocument
from schools.models import School, Campus, Program

class ApplicationForm(forms.ModelForm):
    """Form for bursary application"""
    class Meta:
        model = Application
        fields = ['school', 'campus', 'program', 'admission_number', 'year_of_study', 
                  'family_income', 'amount_requested', 'reason']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'campus': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'family_income': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['campus'].required = False
        # Filter active schools and programs
        self.fields['school'].queryset = School.objects.filter(is_active=True)
        self.fields['program'].queryset = Program.objects.filter(is_active=True)


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
            # Limit file size to 5MB
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size cannot exceed 5MB')
        return file
