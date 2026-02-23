from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.db import models
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import csv
import logging
from django.http import HttpResponse

from applications.models import Application, ApplicationApproval
from users.models import AdminRole
from notifications.services import NotificationService

logger = logging.getLogger(__name__)


def is_admin(user):
    """Check if user is admin - allows superusers, staff with admin_role, or is_staff users"""
    # Allow superusers
    if user.is_superuser:
        return True
    
    # Allow staff users with proper admin role
    if user.is_staff:
        # Try to get the admin role
        try:
            return hasattr(user, 'admin_role') and user.admin_role.is_active
        except:
            # Staff user without admin role - grant access for Super Admin
            return True
    
    return False


def get_admin_role_type(user):
    """Safely get admin role type - returns 'Super_Admin' for superusers, or the role_type if exists"""
    if user.is_superuser:
        return 'Super_Admin'
    
    try:
        if hasattr(user, 'admin_role') and user.admin_role:
            return user.admin_role.role_type
    except:
        pass
    
    return 'Super_Admin'  # Default to Super Admin for staff without role


@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access the admin panel. Your account may not be fully configured as an admin.')
        # Show a simple error page instead of redirecting (to avoid loops)
        return render(request, 'admin_panel/access_denied.html', {
            'message': 'Admin access required. Please contact a Super Admin to configure your account.'
        })
    
    # Get statistics
    total_applications = Application.objects.count()
    pending_review = Application.objects.filter(status__in=['Submitted', 'Under_Review']).count()
    approved = Application.objects.filter(status='Approved').count()
    rejected = Application.objects.filter(status='Rejected').count()
    
    # Recent applications
    recent_apps = Application.objects.all().select_related('applicant', 'school').order_by('-submitted_date')[:10]
    
    # Get admin's ward applications (if ward admin)
    # Get admin role safely - Super Admin won't have AdminRole
    admin_role = None
    try:
        admin_role = request.user.admin_role
        if admin_role.role_type == 'Ward_Admin':
            applications = Application.objects.filter(
                applicant__profile__ward=admin_role.ward
            )
            pending_review = applications.filter(status__in=['Submitted', 'Under_Review']).count()
    except:
        # Super Admin or no admin role - show all applications
        pass
    
    context = {
        'total_applications': total_applications,
        'pending_review': pending_review,
        'approved': approved,
        'rejected': rejected,
        'recent_applications': recent_apps,
        'admin_role': admin_role,
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
    
    # Filter by ward if ward admin (Super Admin sees all)
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type == 'Ward_Admin':
        try:
            applications = applications.filter(applicant__profile__ward=request.user.admin_role.ward)
        except:
            pass
    
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
    # Permission check
    if not is_admin(request.user):
        logger.warning(f"Unauthorized approval attempt by {request.user.username} for application {application_id}")
        messages.error(request, 'You do not have permission to approve applications.')
        return redirect('applications:dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    
    # Check ward access for ward admins (Super Admin can approve any)
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type == 'Ward_Admin':
        try:
            if application.applicant.profile.ward != request.user.admin_role.ward:
                logger.warning(f"Ward admin {request.user.username} tried to approve application from different ward")
                messages.error(request, 'You can only approve applications from your assigned ward.')
                return redirect('admin_panel:applications_review')
        except:
            pass
    
    if request.method == 'POST':
        try:
            comments = request.POST.get('comments', '')
            
            if not comments or comments.strip() == '':
                messages.error(request, 'Please provide verification comments.')
                return render(request, 'admin_panel/approve_application.html', {'application': application})
            
            logger.info(f"Approving application {application_id} by {request.user.username}.")
            
            # Create approval record (ward admin approval - no amount set yet)
            approval = ApplicationApproval.objects.create(
                application=application,
                approved_by=request.user,
                approval_level=get_admin_role_type(request.user),
                status='Approved',
                reason=comments,
                amount_approved=None  # CDF Admin will set amount later
            )
            logger.info(f"Approval record created: {approval.id}")
            
            # Update application status
            application.status = 'Approved'
            application.reviewed_by = request.user
            application.reviewed_date = timezone.now()
            application.save()
            logger.info(f"Application {application_id} status updated to Approved")
            
            # Send notification
            try:
                NotificationService.send_application_approved_notification(application)
                logger.info(f"Notification sent for application {application_id}")
            except Exception as e:
                logger.error(f"Failed to send notification: {str(e)}")
            
            messages.success(
                request, 
                f'Application approved successfully! Documents verified. Application forwarded to CDF Office for final amount approval.'
            )
            return redirect('admin_panel:applications_review')
            
        except Exception as e:
            logger.error(f"Error approving application {application_id}: {str(e)}", exc_info=True)
            messages.error(request, f'Error approving application: {str(e)}')
            return redirect('admin_panel:applications_review')
    
    context = {'application': application}
    return render(request, 'admin_panel/approve_application.html', context)


@login_required
def reject_application(request, application_id):
    """Reject an application"""
    # Permission check
    if not is_admin(request.user):
        logger.warning(f"Unauthorized rejection attempt by {request.user.username} for application {application_id}")
        messages.error(request, 'You do not have permission to reject applications.')
        return redirect('applications:dashboard')
    
    # Verify user is admin
    if not hasattr(request.user, 'admin_role'):
        logger.error(f"User {request.user.username} has is_staff=True but no AdminRole")
        messages.error(request, 'Your admin role is not configured properly.')
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    
    # Check ward access for ward admins
    if request.user.admin_role.role_type == 'Ward_Admin':
        if application.applicant.profile.ward != request.user.admin_role.ward:
            logger.warning(f"Ward admin {request.user.username} tried to reject application from different ward")
            messages.error(request, 'You can only reject applications from your assigned ward.')
            return redirect('admin_panel:applications_review')
    
    if request.method == 'POST':
        try:
            reason = request.POST.get('reason', '')
            
            if not reason or reason.strip() == '':
                messages.error(request, 'Please provide a reason for rejection.')
                return render(request, 'admin_panel/reject_application.html', {'application': application})
            
            logger.info(f"Rejecting application {application_id} by {request.user.username}")
            
            # Create approval record
            rejection = ApplicationApproval.objects.create(
                application=application,
                approved_by=request.user,
                approval_level=request.user.admin_role.role_type,
                status='Rejected',
                reason=reason
            )
            logger.info(f"Rejection record created: {rejection.id}")
            
            # Update application status
            application.status = 'Rejected'
            application.reviewed_by = request.user
            application.reviewed_date = timezone.now()
            application.save()
            logger.info(f"Application {application_id} status updated to Rejected")
            
            # Send notification
            try:
                NotificationService.send_application_rejected_notification(application)
                logger.info(f"Rejection notification sent for application {application_id}")
            except Exception as e:
                logger.error(f"Failed to send rejection notification: {str(e)}")
            
            messages.success(request, 'Application rejected successfully. Applicant has been notified.')
            return redirect('admin_panel:applications_review')
            
        except Exception as e:
            logger.error(f"Error rejecting application {application_id}: {str(e)}", exc_info=True)
            messages.error(request, f'Error rejecting application: {str(e)}')
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
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type == 'Ward_Admin':
        try:
            approved_apps = approved_apps.filter(applicant__profile__ward=request.user.admin_role.ward)
        except:
            pass
    
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
    
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type == 'Ward_Admin':
        try:
            approved_apps = approved_apps.filter(applicant__profile__ward=request.user.admin_role.ward)
        except:
            pass
    
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


@login_required
def cdf_approved_applications(request):
    """CDF Admin view - List of Ward-approved applications waiting for amount award"""
    if not is_admin(request.user):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('applications:dashboard')
    
    # Check if user is CDF_Admin
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type != 'CDF_Admin':
        messages.error(request, 'Only CDF Admins can award amounts.')
        return redirect('admin_panel:dashboard')
    
    # Get selected ward from query parameter
    selected_ward = request.GET.get('ward', '')
    
    # Get all approved applications (approved by ward admin, awaiting amount)
    approved_applications = Application.objects.filter(
        status='Approved'
    ).select_related('applicant', 'school', 'program').order_by('-reviewed_date')
    
    # Filter by ward if selected
    if selected_ward:
        approved_applications = approved_applications.filter(applicant__profile__ward=selected_ward)
    
    # Get ward-wise statistics
    ward_choices = [
        ('Mayoni', 'Mayoni'),
        ('Kholera', 'Kholera'),
        ('Khalaba', 'Khalaba'),
        ('Koyonzo', 'Koyonzo'),
        ('Namamali', 'Namamali'),
    ]
    
    ward_stats = []
    for ward_value, ward_name in ward_choices:
        count = Application.objects.filter(
            status='Approved',
            applicant__profile__ward=ward_value
        ).count()
        
        # Get applications with approved amounts via ApplicationApproval model
        awarded_count = Application.objects.filter(
            status='Approved',
            applicant__profile__ward=ward_value,
            approvals__amount_approved__isnull=False,
            approvals__status='Approved'
        ).distinct().count()
        
        # Sum approved amounts from ApplicationApproval model
        from applications.models import ApplicationApproval
        total_awarded = ApplicationApproval.objects.filter(
            application__status='Approved',
            application__applicant__profile__ward=ward_value,
            status='Approved',
            amount_approved__isnull=False
        ).aggregate(total=models.Sum('amount_approved'))['total'] or 0
        
        ward_stats.append({
            'ward': ward_value,
            'ward_name': ward_name,
            'total_applicants': count,
            'total_awarded': total_awarded,
            'awarded_count': awarded_count,
            'pending_count': count - awarded_count,
        })
    
    context = {
        'applications': approved_applications,
        'total': approved_applications.count(),
        'ward_stats': ward_stats,
        'selected_ward': selected_ward,
        'ward_choices': ward_choices,
    }
    return render(request, 'admin_panel/cdf_approved_applications.html', context)


@login_required
def award_application_amount(request, application_id):
    """CDF Admin - Award amount to an approved application"""
    if not is_admin(request.user):
        logger.warning(f"Unauthorized amount award attempt by {request.user.username}")
        messages.error(request, 'Permission denied.')
        return redirect('applications:dashboard')
    
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type != 'CDF_Admin':
        logger.warning(f"Non-CDF admin {request.user.username} tried to award amount")
        messages.error(request, 'Only CDF Admins can award amounts.')
        return redirect('admin_panel:dashboard')
    
    application = get_object_or_404(Application, id=application_id)
    
    if application.status != 'Approved':
        messages.error(request, 'Only Ward-approved applications can receive amount award.')
        return redirect('admin_panel:cdf_approved_applications')
    
    if request.method == 'POST':
        try:
            amount = request.POST.get('amount_awarded', '')
            cdf_comments = request.POST.get('cdf_comments', '')
            
            if not amount or float(amount) <= 0:
                messages.error(request, 'Please enter a valid amount.')
                return render(request, 'admin_panel/award_amount.html', {'application': application})
            
            amount = float(amount)
            
            logger.info(f"CDF Admin {request.user.username} awarding KES {amount} to application {application_id}")
            
            # Create CDF approval record with amount
            cdf_approval = ApplicationApproval.objects.create(
                application=application,
                approved_by=request.user,
                approval_level='CDF_Admin',
                status='Approved',
                amount_approved=amount,
                reason=cdf_comments
            )
            logger.info(f"CDF approval record created: {cdf_approval.id} with amount: {amount}")
            
            logger.info(f"Application {application_id} awarded final amount: KES {amount}")
            
            messages.success(
                request,
                f'Amount awarded successfully! KES {amount:,.2f} awarded to {application.applicant.get_full_name()}'
            )
            return redirect('admin_panel:cdf_approved_applications')
            
        except ValueError:
            messages.error(request, 'Please enter a valid number for amount.')
            return render(request, 'admin_panel/award_amount.html', {'application': application})
        except Exception as e:
            logger.error(f"Error awarding amount for application {application_id}: {str(e)}", exc_info=True)
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:cdf_approved_applications')
    
    context = {'application': application}
    return render(request, 'admin_panel/award_amount.html', context)


@login_required
def registration_settings(request):
    """CDF Admin - Manage registration settings"""
    if not is_admin(request.user):
        messages.error(request, 'Permission denied.')
        return redirect('applications:dashboard')
    
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type != 'CDF_Admin':
        messages.error(request, 'Only CDF Admins can manage registration settings.')
        return redirect('admin_panel:dashboard')
    
    from applications.models import RegistrationSettings
    import uuid
    
    # Get or create default settings (only one record in the system)
    settings = RegistrationSettings.objects.first()
    if not settings:
        settings = RegistrationSettings.objects.create()
    
    if request.method == 'POST':
        is_open = request.POST.get('is_registration_open') == 'on'
        deadline = request.POST.get('deadline_date')
        
        settings.is_registration_open = is_open
        if deadline:
            from django.utils.dateparse import parse_datetime
            settings.deadline_date = parse_datetime(deadline) if deadline else None
        else:
            settings.deadline_date = None
        
        settings.save()
        logger.info(f"Registration settings updated by {request.user.username}: Open={is_open}, Deadline={deadline}")
        messages.success(request, 'Registration settings updated successfully!')
        return redirect('admin_panel:registration_settings')
    
    context = {
        'settings': settings,
    }
    return render(request, 'admin_panel/registration_settings.html', context)


@login_required
def rejected_applicants(request):
    """CDF Admin - View rejected applicants by ward"""
    if not is_admin(request.user):
        messages.error(request, 'Permission denied.')
        return redirect('applications:dashboard')
    
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type != 'CDF_Admin':
        messages.error(request, 'Only CDF Admins can view this page.')
        return redirect('admin_panel:dashboard')
    
    # Get selected ward from query parameter
    selected_ward = request.GET.get('ward', '')
    
    # Get all rejected applications
    rejected_applications = Application.objects.filter(
        status='Rejected'
    ).select_related('applicant', 'school', 'program').order_by('-reviewed_date')
    
    # Get rejection reasons from ApplicationApproval
    rejected_apps_with_reason = []
    for app in rejected_applications:
        rejection = app.approvals.filter(status='Rejected').first()
        if rejection:
            rejected_apps_with_reason.append({
                'app': app,
                'rejection_reason': rejection.reason,
                'rejection_date': rejection.approved_date,
                'rejected_by': rejection.approved_by,
            })
    
    # Filter by ward if selected
    if selected_ward:
        rejected_apps_with_reason = [
            item for item in rejected_apps_with_reason 
            if item['app'].applicant.profile.ward == selected_ward
        ]
    
    # Get ward-wise statistics for rejected applicants
    ward_choices = [
        ('Mayoni', 'Mayoni'),
        ('Kholera', 'Kholera'),
        ('Khalaba', 'Khalaba'),
        ('Koyonzo', 'Koyonzo'),
        ('Namamali', 'Namamali'),
    ]
    
    ward_stats = []
    for ward_value, ward_name in ward_choices:
        count = Application.objects.filter(
            status='Rejected',
            applicant__profile__ward=ward_value
        ).count()
        
        ward_stats.append({
            'ward': ward_value,
            'ward_name': ward_name,
            'rejected_count': count,
        })
    
    context = {
        'rejected_apps_with_reason': rejected_apps_with_reason,
        'total': len(rejected_apps_with_reason),
        'ward_stats': ward_stats,
        'selected_ward': selected_ward,
        'ward_choices': ward_choices,
    }
    return render(request, 'admin_panel/rejected_applicants.html', context)


@login_required
def export_approved_applicants(request):
    """CDF Admin - Export approved applicants to CSV"""
    if not is_admin(request.user):
        logger.warning(f"Unauthorized export attempt by {request.user.username}")
        return HttpResponse('Permission denied', status=403)
    
    admin_role_type = get_admin_role_type(request.user)
    if admin_role_type != 'CDF_Admin':
        logger.warning(f"Non-CDF admin export attempt by {request.user.username}")
        return HttpResponse('Only CDF Admins can export data', status=403)
    
    # Get selected ward from query parameter
    selected_ward = request.GET.get('ward', '')
    
    # Get all approved applications
    approved_applications = Application.objects.filter(
        status='Approved'
    ).select_related('applicant', 'school', 'applicant__profile').prefetch_related('approvals').order_by('applicant__last_name', 'applicant__first_name')
    
    # Filter by ward if selected
    if selected_ward:
        approved_applications = approved_applications.filter(
            applicant__profile__ward=selected_ward
        )
    
    # Create CSV file
    response = HttpResponse(content_type='text/csv')
    filename = f'approved_applicants_{selected_ward or "all"}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Full Name', 'School', 'National ID', 'Amount Awarded (KES)', 
        'Ward', 'Email', 'Phone', 'Application Date', 'Approval Date'
    ])
    
    for app in approved_applications:
        # Get the approved amount from ApplicationApproval model
        approved_amount = app.approvals.filter(
            status='Approved',
            amount_approved__isnull=False
        ).order_by('-approved_date').first()
        
        writer.writerow([
            app.applicant.get_full_name(),
            app.school.name,
            app.national_id,
            approved_amount.amount_approved if approved_amount else 'Pending',
            app.applicant.profile.ward,
            app.applicant.email,
            app.phone_number,
            app.submitted_date.strftime('%Y-%m-%d') if app.submitted_date else '',
            app.reviewed_date.strftime('%Y-%m-%d') if app.reviewed_date else '',
        ])
    
    logger.info(f"Export approved applicants ({selected_ward or 'all'} ward) by {request.user.username}")
    return response
