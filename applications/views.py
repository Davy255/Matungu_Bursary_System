from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, FileResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from django.contrib.auth.models import User

from .models import Application, ApplicationDocument, ApplicationReview, ApplicationComment, ApplicationApproval
from .forms import (
    ApplicationForm, ApplicationDocumentForm, SchoolSelectionForm,
    ApplicationReviewForm, ApplicationCommentForm, ApplicationFilterForm, DocumentFormSet,
    UpdateWardForm
)
from schools.models import School, SchoolCategory, Campus, Program
from notifications.services import NotificationService


def ensure_user_profile(user):
    """Ensure user has a profile, create if doesn't exist"""
    from users.models import UserProfile
    if not hasattr(user, 'profile'):
        UserProfile.objects.get_or_create(user=user)
    return user.profile


@login_required
def applicant_dashboard(request):
    """Applicant dashboard showing their applications"""
    profile = ensure_user_profile(request.user)
    
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    applications = Application.objects.filter(applicant=request.user).select_related('school', 'program', 'ward')
    
    # Get statistics
    stats = {
        'total': applications.count(),
        'draft': applications.filter(status='Draft').count(),
        'submitted': applications.filter(status='Submitted').count(),
        'approved': applications.filter(status='Approved').count(),
        'rejected': applications.filter(status='Rejected').count(),
        'without_ward': applications.filter(ward__isnull=True).count(),
    }
    
    # Get applications without ward for the warning
    apps_without_ward = applications.filter(ward__isnull=True)
    
    # Pagination
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'stats': stats,
        'apps_without_ward': apps_without_ward,
    }
    return render(request, 'applications/applicant_dashboard.html', context)


@login_required
def new_application_step1(request):
    """Step 1: Select school category and school"""
    profile = ensure_user_profile(request.user)
    
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        school_id = request.POST.get('school')
        
        if not all([category_id, school_id]):
            messages.error(request, 'Please select category and school.')
            return redirect('applications:new_step1')
        
        # Create draft application
        school = get_object_or_404(School, id=school_id)
        
        # Auto-select the default program (General Studies) for the school
        program = Program.objects.filter(school=school, name='General Studies').first()
        if not program:
            # If no General Studies program exists, get the first available program
            program = Program.objects.filter(school=school, is_active=True).first()
        
        if not program:
            messages.error(request, 'No programs available for this school. Please contact administrator.')
            return redirect('applications:new_step1')
        
        application = Application.objects.create(
            applicant=request.user,
            school=school,
            program=program,
            status='Draft'
        )
        
        messages.success(request, 'School selection saved. Now fill in your details.')
        return redirect('applications:new_step2', application_id=application.id)
    
    categories = SchoolCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'applications/new_application_step1.html', context)


@login_required
def new_application_step2(request, application_id):
    """Step 2: Fill application form"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application details saved. Now upload required documents.')
            return redirect('applications:new_step3', application_id=application.id)
    else:
        form = ApplicationForm(instance=application)
    
    context = {
        'form': form,
        'application': application,
        'school': application.school,
    }
    return render(request, 'applications/new_application_step2.html', context)


@login_required
def new_application_step3(request, application_id):
    """Step 3: Upload documents"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == 'POST':
        form = ApplicationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.application = application
            doc.save()
            messages.success(request, f'{doc.get_document_type_display()} uploaded successfully.')
            return redirect('applications:new_step3', application_id=application.id)
        else:
            # Form has errors, display them
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ApplicationDocumentForm()
    
    documents = application.documents.all()
    context = {
        'application': application,
        'documents': documents,
        'form': form,
    }
    return render(request, 'applications/new_application_step3.html', context)


@login_required
def new_application_step4(request, application_id):
    """Step 4: Review and submit application"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    documents = application.documents.all()
    
    if request.method == 'POST':
        application.status = 'Submitted'
        application.submitted_date = timezone.now()
        application.save()
        
        # Send notifications
        try:
            NotificationService.send_application_submitted_notification(application)
        except Exception as e:
            print(f"Error sending notification: {e}")
        
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('applications:dashboard')
    
    context = {
        'application': application,
        'documents': documents,
    }
    return render(request, 'applications/new_application_step4.html', context)


@login_required
def application_detail(request, application_id):
    """View application details"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check permissions
    if request.user != application.applicant and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('applications:dashboard')
    
    documents = application.documents.all()
    comments = application.comments.filter(is_internal=False)
    
    if hasattr(application, 'review'):
        review = application.review
    else:
        review = None
    
    context = {
        'application': application,
        'documents': documents,
        'comments': comments,
        'review': review,
    }
    return render(request, 'applications/application_detail.html', context)


@login_required
def upload_document(request, application_id):
    """Upload document for application"""
    if request.method == 'POST' and request.FILES:
        application = get_object_or_404(Application, id=application_id)
        
        # Check permission
        if request.user != application.applicant:
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
        document_type = request.POST.get('document_type')
        file = request.FILES.get('file')
        
        if not document_type or not file:
            return JsonResponse({'status': 'error', 'message': 'Missing document type or file'}, status=400)
        
        # Check if document type already exists
        if ApplicationDocument.objects.filter(application=application, document_type=document_type).exists():
            ApplicationDocument.objects.filter(application=application, document_type=document_type).delete()
        
        doc = ApplicationDocument.objects.create(
            application=application,
            document_type=document_type,
            file=file
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Document uploaded successfully',
            'document_id': str(doc.id)
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def delete_document(request, doc_id):
    """Delete a document from an application"""
    doc = get_object_or_404(ApplicationDocument, id=doc_id)
    
    # Check permission - user must be the applicant
    if request.user != doc.application.applicant:
        messages.error(request, 'Permission denied.')
        return redirect('applications:dashboard')
    
    # Only allow deletion if application is still in Draft or Submitted status
    if doc.application.status not in ['Draft', 'Submitted']:
        messages.error(request, 'Cannot delete documents from applications under review.')
        return redirect('applications:new_step3', application_id=doc.application.id)
    
    application_id = doc.application.id
    doc.delete()
    messages.success(request, 'Document deleted successfully.')
    return redirect('applications:new_step3', application_id=application_id)


@login_required
def update_ward(request, application_id):
    """Allow users to update their ward - available for all application statuses"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    if request.method == 'POST':
        form = UpdateWardForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward updated successfully.')
            return redirect('applications:detail', application_id=application.id)
    else:
        form = UpdateWardForm(instance=application)
    
    context = {
        'form': form,
        'application': application,
    }
    return render(request, 'applications/update_ward.html', context)


@login_required
def delete_application(request, application_id):
    """Delete a draft application"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    # Only allow deletion of draft applications
    if application.status != 'Draft':
        messages.error(request, 'Only draft applications can be deleted.')
        return redirect('applications:dashboard')
    
    if request.method == 'POST':
        school_name = application.school.name
        application.delete()
        messages.success(request, f'Draft application for {school_name} has been deleted.')
        return redirect('applications:dashboard')
    
    # If GET request, show confirmation page
    context = {
        'application': application,
    }
    return render(request, 'applications/delete_application_confirm.html', context)


# ADMIN VIEWS

@login_required
def admin_applications_list(request):
    """Admin view to list all applications for review"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    applications = Application.objects.filter(status__in=['Submitted', 'Under_Review']).select_related('applicant', 'school')
    
    # Filtering
    form = ApplicationFilterForm(request.GET or None)
    if form.is_valid():
        if form.cleaned_data.get('status'):
            applications = applications.filter(status__in=form.cleaned_data['status'])
        if form.cleaned_data.get('school'):
            applications = applications.filter(school__name__icontains=form.cleaned_data['school'])
        if form.cleaned_data.get('date_from'):
            applications = applications.filter(submitted_date__gte=form.cleaned_data['date_from'])
        if form.cleaned_data.get('date_to'):
            applications = applications.filter(submitted_date__lte=form.cleaned_data['date_to'])
        if form.cleaned_data.get('search'):
            search = form.cleaned_data['search']
            applications = applications.filter(
                Q(applicant__first_name__icontains=search) |
                Q(applicant__last_name__icontains=search) |
                Q(applicant__profile__national_id__icontains=search)
            )
    
    # Pagination
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'form': form,
        'total_pending': Application.objects.filter(status__in=['Submitted', 'Under_Review']).count(),
    }
    return render(request, 'admin_panel/applications_list.html', context)


@login_required
def admin_review_application(request, application_id):
    """Admin view to review and approve/reject application"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    documents = application.documents.all()
    
    # Get or create review
    review, created = ApplicationReview.objects.get_or_refund(application=application, defaults={
        'reviewer': request.user
    })
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application
            review.reviewer = request.user
            review.review_status = 'Completed'
            review.save()
            
            # Update application status based on recommendation
            if review.recommendation == 'Approve':
                application.status = 'Approved'
                ApplicationApproval.objects.create(
                    application=application,
                    approved_by=request.user,
                    approval_level='Under_Review',
                    status='Approved'
                )
            elif review.recommendation == 'Reject':
                application.status = 'Rejected'
                ApplicationApproval.objects.create(
                    application=application,
                    approved_by=request.user,
                    approval_level='Under_Review',
                    status='Rejected',
                    reason=review.comments
                )
            elif review.recommendation == 'Clarify':
                application.status = 'Needs_Clarification'
            
            application.reviewed_by = request.user
            application.reviewed_date = timezone.now()
            application.save()
            
            messages.success(request, 'Application review submitted successfully!')
            return redirect('admin_panel:applications_list')
    else:
        form = ApplicationReviewForm(instance=review)
    
    context = {
        'application': application,
        'documents': documents,
        'form': form,
        'review': review,
    }
    return render(request, 'admin_panel/review_application.html', context)


@login_required
def add_application_comment(request, application_id):
    """Add comment to application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check permission
    if request.user != application.applicant and not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        form = ApplicationCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.application = application
            comment.commented_by = request.user
            comment.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Comment added successfully',
                'comment': {
                    'id': str(comment.id),
                    'text': comment.comment,
                    'author': request.user.get_full_name(),
                    'date': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                }
            })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def track_application(request):
    """Track application status"""
    profile = ensure_user_profile(request.user)
    if profile.user_type != 'Applicant':
        return redirect('admin_panel:dashboard')
    
    applications = Application.objects.filter(applicant=request.user).order_by('-submitted_date')
    
    # Calculate stats for each status
    approved_count = applications.filter(status='Approved').count()
    rejected_count = applications.filter(status='Rejected').count()
    under_review_count = applications.filter(status__in=['Submitted', 'Under_Review']).count()
    
    context = {
        'applications': applications,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'under_review_count': under_review_count,
    }
    return render(request, 'applications/track_application.html', context)


@login_required
def export_approved_applications(request):
    """Export list of approved applicants as PDF"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this resource.')
        return redirect('applications:dashboard')
    
    approved_apps = Application.objects.filter(status='Approved').select_related('applicant', 'school', 'program')
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="approved_applicants.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
    )
    
    # Title
    title = Paragraph("Approved Bursary Applicants<br/>Matungu Subcounty, Kakamega County", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Export date
    date_text = Paragraph(f"Export Date: {timezone.now().strftime('%d %B %Y')}", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Data for table
    data = [['No.', 'Full Name', 'School', 'Program', 'Phone Number', 'Email']]
    
    for idx, app in enumerate(approved_apps, 1):
        data.append([
            str(idx),
            app.applicant.get_full_name(),
            app.school.name,
            app.program.name,
            app.phone_number,
            app.email,
        ])
    
    # Create table
    table = Table(data, colWidths=[0.6*inch, 2*inch, 1.8*inch, 1.5*inch, 1.2*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary
    summary_text = Paragraph(
        f"<b>Total Approved Applicants: {approved_apps.count()}</b><br/>"
        f"Report generated on {timezone.now().strftime('%d %B %Y at %H:%M')}",
        styles['Normal']
    )
    elements.append(summary_text)
    
    doc.build(elements)
    return response


# Alias for compatibility
@login_required
def dashboard(request):
    """Redirect to appropriate dashboard based on user role"""
    profile = ensure_user_profile(request.user)
    
    if profile.user_type == 'Applicant':
        return applicant_dashboard(request)
    else:
        return redirect('admin_panel:dashboard')
