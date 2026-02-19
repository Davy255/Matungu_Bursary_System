from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from applications.models import Application
from notifications.services import NotificationService


class Command(BaseCommand):
    help = 'Test notification system by sending test notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the applicant',
            required=False
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['submitted', 'approved', 'rejected'],
            default='submitted',
            help='Type of notification to test (submitted/approved/rejected)'
        )

    def handle(self, *args, **options):
        username = options.get('username')
        notification_type = options.get('type')
        
        # Get user
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
                return
        else:
            # List users with applications
            users_with_apps = User.objects.filter(applications__isnull=False).distinct()
            if not users_with_apps.exists():
                self.stdout.write(self.style.ERROR('No users with applications found'))
                return
            
            self.stdout.write('\nUsers with applications:')
            for i, u in enumerate(users_with_apps, 1):
                app_count = u.applications.count()
                self.stdout.write(f'{i}. {u.username} ({u.get_full_name() or "No name"}) - {app_count} application(s)')
            
            # Use first user if only one
            if users_with_apps.count() == 1:
                user = users_with_apps.first()
                self.stdout.write(f'\nUsing user: {user.username}')
            else:
                self.stdout.write(self.style.WARNING('\nPlease specify --username=<username>'))
                return
        
        # Get user's most recent application
        application = user.applications.order_by('-created_at').first()
        
        if not application:
            self.stdout.write(self.style.ERROR(f'No applications found for user {user.username}'))
            return
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'Testing {notification_type.upper()} notification'))
        self.stdout.write('='*70)
        
        self.stdout.write(f'\nApplication Details:')
        self.stdout.write(f'  User: {user.username} ({user.get_full_name() or "No name"})')
        self.stdout.write(f'  School: {application.school.name}')
        self.stdout.write(f'  Program: {application.program.name}')
        self.stdout.write(f'  Email: {application.email or user.email or "Not provided"}')
        self.stdout.write(f'  Phone: {application.phone_number or "Not provided"}')
        
        # Check notification preferences
        preference = getattr(user, 'notification_preference', None)
        if preference:
            self.stdout.write(f'\nNotification Preferences:')
            if notification_type == 'submitted':
                self.stdout.write(f'  Email on submission: {"✓ Enabled" if preference.email_on_submission else "✗ Disabled"}')
                self.stdout.write(f'  SMS on submission: {"✓ Enabled" if preference.sms_on_submission else "✗ Disabled"}')
            elif notification_type == 'approved':
                self.stdout.write(f'  Email on approval: {"✓ Enabled" if preference.email_on_approval else "✗ Disabled"}')
                self.stdout.write(f'  SMS on approval: {"✓ Enabled" if preference.sms_on_approval else "✗ Disabled"}')
            elif notification_type == 'rejected':
                self.stdout.write(f'  Email on rejection: {"✓ Enabled" if preference.email_on_rejection else "✗ Disabled"}')
                self.stdout.write(f'  SMS on rejection: {"✓ Enabled" if preference.sms_on_rejection else "✗ Disabled"}')
        else:
            self.stdout.write(self.style.WARNING('\n⚠ No notification preferences found - creating default preferences'))
            from notifications.models import NotificationPreference
            NotificationPreference.objects.get_or_create(user=user)
        
        self.stdout.write('\n' + '-'*70)
        self.stdout.write('Sending notifications...\n')
        
        try:
            # Send the appropriate notification
            if notification_type == 'submitted':
                NotificationService.send_application_submitted_notification(application)
            elif notification_type == 'approved':
                NotificationService.send_application_approved_notification(application)
            elif notification_type == 'rejected':
                NotificationService.send_application_rejected_notification(application)
            
            self.stdout.write('\n' + '='*70)
            self.stdout.write(self.style.SUCCESS('✅ Notification test completed!'))
            self.stdout.write('='*70)
            self.stdout.write('\nCheck above for:')
            self.stdout.write('  • Email content (in console since EMAIL_BACKEND=console)')
            self.stdout.write('  • SMS message preview')
            self.stdout.write('  • Any error messages')
            self.stdout.write('\nTo send real emails/SMS, configure your .env file with:')
            self.stdout.write('  EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (for emails)')
            self.stdout.write('  TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN (for SMS)')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())
