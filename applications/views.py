from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Application, ApplicationDocument, BursarySettings
from .forms import ApplicationForm, ApplicationDocumentForm
from schools.models import School
import uuid
import json


def _schools_json():
    """Build schools-by-category dict for JS autocomplete."""
    schools_by_category = {}
    for school in School.objects.filter(is_active=True).values('id', 'name', 'school_type').order_by('name'):
        cat = school['school_type']
        schools_by_category.setdefault(cat, [])
        schools_by_category[cat].append({'id': school['id'], 'name': school['name']})
    return json.dumps(schools_by_category)


def _save_draft(post_data, user, application=None):
    """Save (or update) a draft from raw POST data without full validation."""
    if application is None:
        application = Application(
            applicant=user,
            application_number=f"BUR-{timezone.now().year}-{uuid.uuid4().hex[:8].upper()}",
            status='draft',
        )

    # School FK
    school_id = post_data.get('school', '').strip()
    if school_id:
        try:
            application.school = School.objects.get(pk=int(school_id))
        except (School.DoesNotExist, ValueError):
            application.school = None
    else:
        application.school = None

    application.course_name      = post_data.get('course_name', '').strip()
    application.admission_number = post_data.get('admission_number', '').strip()
    application.year_of_study    = post_data.get('year_of_study', '').strip()

    # Numeric fields — keep existing value if blank
    for attr, key in [('family_income', 'family_income'), ('amount_requested', 'amount_requested')]:
        val = post_data.get(key, '').strip()
        if val:
            try:
                setattr(application, attr, float(val))
            except ValueError:
                pass

    application.reason = post_data.get('reason', '').strip()
    application.save()
    return application


@login_required
def apply(request):
    """Create new bursary application."""
    if not hasattr(request.user, 'profile'):
        messages.warning(request, 'Please complete your profile before applying.')
        return redirect('users:profile')

    settings_obj = BursarySettings.get_settings()
    if not settings_obj.is_accepting_applications:
        messages.error(request, 'Applications are currently closed.')
        return redirect('users:dashboard')

    # One application per user — redirect to existing one
    existing = Application.objects.filter(applicant=request.user).order_by('-created_at').first()
    if existing:
        if existing.status == 'draft':
            messages.info(request, 'You have an unfinished draft. Please complete it before starting a new one.')
            return redirect('applications:edit_draft', pk=existing.pk)
        else:
            messages.warning(request,
                f'You already have an application ({existing.application_number}). '
                'Only one application per person is allowed per cycle.')
            return redirect('applications:view_application', pk=existing.pk)

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')

        if action == 'save_draft':
            application = _save_draft(request.POST, request.user)
            messages.success(request, 'Draft saved! You can continue editing it from your dashboard.')
            return redirect('users:dashboard')

        # Full submit path
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.application_number = f"BUR-{timezone.now().year}-{uuid.uuid4().hex[:8].upper()}"
            application.status = 'draft'
            application.save()
            messages.success(request, 'Application saved! Please upload required documents.')
            return redirect('applications:upload_documents', pk=application.pk)
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {
        'form': form,
        'schools_json': _schools_json(),
        'settings': settings_obj,
    })


@login_required
def edit_draft(request, pk):
    """Continue editing a saved draft."""
    application = get_object_or_404(Application, pk=pk, applicant=request.user, status='draft')

    settings_obj = BursarySettings.get_settings()
    if not settings_obj.is_accepting_applications:
        messages.error(request, 'Applications are currently closed.')
        return redirect('users:dashboard')

    if request.method == 'POST':
        action = request.POST.get('action', 'submit')

        if action == 'save_draft':
            _save_draft(request.POST, request.user, application=application)
            messages.success(request, 'Draft updated! You can continue editing from your dashboard.')
            return redirect('users:dashboard')

        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            app = form.save(commit=False)
            app.status = 'draft'
            app.save()
            messages.success(request, 'Application updated! Please upload / review required documents.')
            return redirect('applications:upload_documents', pk=application.pk)
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'applications/apply.html', {
        'form': form,
        'schools_json': _schools_json(),
        'application': application,   # lets template know it's an edit
        'settings': settings_obj,
    })

@login_required
def upload_documents(request, pk):
	"""Upload documents for application"""
	application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
	if request.method == 'POST':
		form = ApplicationDocumentForm(request.POST, request.FILES)
		if form.is_valid():
			document = form.save(commit=False)
			document.application = application
			document.file_name = document.file.name
			document.file_size = document.file.size
			document.save()
			messages.success(request, f'{document.get_document_type_display()} uploaded successfully!')
			return redirect('applications:upload_documents', pk=pk)
	else:
		form = ApplicationDocumentForm()
    
	documents = application.documents.all()
	return render(request, 'applications/upload_documents.html', {
		'form': form,
		'application': application,
		'documents': documents
	})

@login_required
def submit_application(request, pk):
	"""Submit application for review"""
	application = get_object_or_404(Application, pk=pk, applicant=request.user)
    
	if application.status != 'draft':
		messages.error(request, 'This application has already been submitted.')
		return redirect('applications:view_application', pk=pk)
    
	# Check if required documents are uploaded
	required_docs = ['id', 'admission', 'fee_structure']
	uploaded_types = list(application.documents.values_list('document_type', flat=True))
	missing = [doc for doc in required_docs if doc not in uploaded_types]
    
	if missing:
		messages.error(request, f'Please upload required documents: {", ".join(missing)}')
		return redirect('applications:upload_documents', pk=pk)
    
	application.status = 'submitted'
	application.submitted_at = timezone.now()
	application.save()
    
	messages.success(request, f'Application {application.application_number} submitted successfully!')
	return redirect('applications:my_applications')

@login_required
def my_applications(request):
	"""View user's applications"""
	applications = Application.objects.filter(applicant=request.user)
	return render(request, 'applications/my_applications.html', {'applications': applications})

@login_required
def view_application(request, pk):
	"""View single application"""
	application = get_object_or_404(Application, pk=pk, applicant=request.user)
	documents = application.documents.all()
	return render(request, 'applications/view_application.html', {
		'application': application,
		'documents': documents
	})

def search_schools(request):
	"""Search for schools"""
	query = request.GET.get('q', '')
	school_type = request.GET.get('type', '')
    
	schools = School.objects.filter(is_active=True)
    
	if query:
		schools = schools.filter(name__icontains=query)
	if school_type:
		schools = schools.filter(school_type=school_type)
    
	return render(request, 'applications/search_schools.html', {
		'schools': schools,
		'query': query,
		'school_type': school_type
	})
