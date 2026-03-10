from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Application, ApplicationDocument
from .forms import ApplicationForm, ApplicationDocumentForm
from schools.models import School
import uuid
import json

@login_required
def apply(request):
	"""Create new bursary application"""
	# Check if user has profile
	if not hasattr(request.user, 'profile'):
		messages.warning(request, 'Please complete your profile before applying.')
		return redirect('users:profile')
    
	if request.method == 'POST':
		form = ApplicationForm(request.POST)
		if form.is_valid():
			application = form.save(commit=False)
			application.applicant = request.user
			application.application_number = f"BUR-{timezone.now().year}-{uuid.uuid4().hex[:8].upper()}"
			application.status = 'draft'
			application.save()
			messages.success(request, 'Application created! Please upload required documents.')
			return redirect('applications:upload_documents', pk=application.pk)
	else:
		form = ApplicationForm()

	# Build schools-by-category JSON for JS filtering
	schools_by_category = {}
	for school in School.objects.filter(is_active=True).values('id', 'name', 'school_type').order_by('name'):
		cat = school['school_type']
		schools_by_category.setdefault(cat, [])
		schools_by_category[cat].append({'id': school['id'], 'name': school['name']})
    
	return render(request, 'applications/apply.html', {
		'form': form,
		'schools_json': json.dumps(schools_by_category),
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
