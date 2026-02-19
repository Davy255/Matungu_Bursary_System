from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import csv
from django.http import HttpResponse

from applications.models import Application, ApplicationApproval
from users.models import AdminRole
from notifications.services import NotificationService


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff and hasattr(user, 'admin_role')


@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    # Get statistics
    total_applications = Application.objects.count()
    pending_review = Application.objects.filter(status__in=['Submitted', 'Under_Review']).count()
    approved = Application.objects.filter(status='Approved').count()
    rejected = Application.objects.filter(status='Rejected').count()
    
    # Recent applications
    recent_apps = Application.objects.all().select_related('applicant', 'school').order_by('-submitted_date')[:10]
    
    # Get admin's ward applications (if ward admin)
    if request.user.admin_role.role_type == 'Ward_Admin':
        applications = Application.objects.filter(
            applicant__profile__ward=request.user.admin_role.ward
        )
        pending_review = applications.filter(status__in=['Submitted', 'Under_Review']).count()
    
    context = {
        'total_applications': total_applications,
        'pending_review': pending_review,
        'approved': approved,
        'rejected': rejected,
        'recent_applications': recent_apps,
        'admin_role': request.user.admin_role,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def applications_for_review(request):
    """List applications pending review for admin"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    applications = Application.objects.filter(
        status__in=['Submitted', 'Under_Review']
    ).select_related('applicant', 'school').order_by('-submitted_date')
    
    # Filter by ward if ward admin
    if request.user.admin_role.role_type == 'Ward_Admin':
        applications = applications.filter(applicant__profile__ward=request.user.admin_role.ward)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'total_pending': applications.count(),
    }
    return render(request, 'admin_panel/applications_for_review.html', context)


@login_required
def approve_application(request, application_id):
    """Approve an application"""
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount_approved', '')
        comments = request.POST.get('comments', '')
        
        # Create approval record
        ApplicationApproval.objects.create(
            application=application,
            approved_by=request.user,
            approval_level=request.user.admin_role.role_type,
            status='Approved',
            reason=comments,
            amount_approved=amount if amount else None
        )
        
        # Update application status
        application.status = 'Approved'
        application.reviewed_by = request.user
        application.reviewed_date = timezone.now()
        application.save()
        
        # Send notification
        NotificationService.send_application_approved_notification(application)
        
        messages.success(request, 'Application approved successfully!')
        return redirect('admin_panel:applications_review')
    
    context = {'application': application}
    return render(request, 'admin_panel/approve_application.html', context)


@login_required
def reject_application(request, application_id):
    """Reject an application"""
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        
        # Create approval record
        ApplicationApproval.objects.create(
            application=application,
            approved_by=request.user,
            approval_level=request.user.admin_role.role_type,
            status='Rejected',
            reason=reason
        )
        
        # Update application status
        application.status = 'Rejected'
        application.reviewed_by = request.user
        application.reviewed_date = timezone.now()
        application.save()
        
        # Send notification
        NotificationService.send_application_rejected_notification(application)
        
        messages.success(request, 'Application rejected successfully!')
        return redirect('admin_panel:applications_review')
    
    context = {'application': application}
    return render(request, 'admin_panel/reject_application.html', context)


@login_required
def approved_applicants_list(request):
    """List all approved applicants for printing/export"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    approved_apps = Application.objects.filter(status='Approved').select_related('applicant', 'school')
    
    # Filter by ward if ward admin
    if request.user.admin_role.role_type == 'Ward_Admin':
        approved_apps = approved_apps.filter(applicant__profile__ward=request.user.admin_role.ward)
    
    context = {
        'applications': approved_apps,
        'total': approved_apps.count(),
    }
    return render(request, 'admin_panel/approved_applicants_list.html', context)


@login_required
def export_approved_csv(request):
    """Export approved applicants as CSV"""
    if not is_admin(request.user):
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    approved_apps = Application.objects.filter(status='Approved').select_related('applicant', 'school')
    
    if request.user.admin_role.role_type == 'Ward_Admin':
        approved_apps = approved_apps.filter(applicant__profile__ward=request.user.admin_role.ward)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="approved_applicants.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['No.', 'Full Name', 'Email', 'Phone', 'School', 'Program', 'Approval Date'])
    
    for idx, app in enumerate(approved_apps, 1):
        writer.writerow([
            idx,
            app.applicant.get_full_name(),
            app.applicant.email,
            app.phone_number,
            app.school.name,
            app.program.name,
            app.reviewed_date.strftime('%d-%m-%Y') if app.reviewed_date else '',
        ])
    
    return response


@login_required
def view_applicant_details(request, application_id):
    """View detailed applicant information"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    documents = application.documents.all()
    approvals = application.approvals.all()
    
    context = {
        'application': application,
        'documents': documents,
        'approvals': approvals,
    }
    return render(request, 'admin_panel/applicant_details.html', context)


@login_required
def manage_admins(request):
    """Super admin view to manage admin roles"""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    admins = AdminRole.objects.all().select_related('user', 'assigned_by')
    
    context = {'admins': admins}
    return render(request, 'admin_panel/manage_admins.html', context)


@login_required
def reports_dashboard(request):
    """Reports and analytics dashboard"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    # Statistics
    total_apps = Application.objects.count()
    approved_count = Application.objects.filter(status='Approved').count()
    rejected_count = Application.objects.filter(status='Rejected').count()
    pending_count = Application.objects.filter(status__in=['Submitted', 'Under_Review']).count()
    
    # Applications by school
    apps_by_school = Application.objects.values('school__name').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Applications by status
    apps_by_status = Application.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_apps': total_apps,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'pending_count': pending_count,
        'apps_by_school': apps_by_school,
        'apps_by_status': apps_by_status,
    }
    return render(request, 'admin_panel/reports.html', context)
