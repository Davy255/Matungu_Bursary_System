from django import forms
from .models import School, SchoolCategory, Campus, Program


class SchoolFilterForm(forms.Form):
    """Form for filtering schools"""
    category = forms.ModelChoiceField(
        queryset=SchoolCategory.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search schools...'
        })
    )


class CampusSelectionForm(forms.Form):
    """Form for selecting a campus"""
    campus = forms.ModelChoiceField(
        queryset=Campus.objects.filter(is_active=True),
        empty_label="Select a campus",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class ProgramSelectionForm(forms.Form):
    """Form for selecting a program"""
    program = forms.ModelChoiceField(
        queryset=Program.objects.filter(is_active=True),
        empty_label="Select a program",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SchoolForm(forms.ModelForm):
    """Admin form for creating/editing schools"""
    class Meta:
        model = School
        fields = ['name', 'category', 'location', 'description', 'code', 
                  'website', 'phone', 'email', 'logo', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CampusForm(forms.ModelForm):
    """Admin form for creating/editing campuses"""
    class Meta:
        model = Campus
        fields = ['name', 'location', 'city', 'is_main_campus', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProgramForm(forms.ModelForm):
    """Admin form for creating/editing programs"""
    class Meta:
        model = Program
        fields = ['name', 'level', 'duration_months', 'tuition_fee', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control'}),
            'tuition_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
