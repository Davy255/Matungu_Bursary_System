from django.core.mail import send_mail
from django.conf import settings
try:
    from twilio.rest import Client  # type: ignore
except ImportError:
    Client = None
from .models import EmailNotification, SMSNotification, NotificationPreference, EmailTemplateContentType, SMSTemplate
from users.models import Notification
from django.utils import timezone


class NotificationService:
    """Service for sending notifications"""
    
    @staticmethod
    def send_application_submitted_notification(application):
        """Send notification when application is submitted"""
        user = application.applicant
        preference = getattr(user, 'notification_preference', None)
        
        if preference:
            if preference.email_on_submission:
                NotificationService.send_email(
                    user,
                    'application_submitted',
                    application,
                    context={'school': application.school.name}
                )
            if preference.sms_on_submission:
                NotificationService.send_sms(
                    user,
                    'application_submitted',
                    application
                )
        
        # Create in-app notification
        Notification.objects.create(
            user=user,
            notification_type='Application_Submitted',
            title='Application Submitted',
            message=f'Your application to {application.school.name} has been submitted successfully.'
        )
    
    @staticmethod
    def send_application_approved_notification(application):
        """Send notification when application is approved"""
        user = application.applicant
        preference = getattr(user, 'notification_preference', None)
        
        # Always send email on approval (unless user explicitly disabled it)
        if not preference or preference.email_on_approval:
            NotificationService.send_email(
                user,
                'application_approved',
                application,
                context={'school': application.school.name, 'applicant_name': user.get_full_name()}
            )
        
        if preference and preference.sms_on_approval:
            NotificationService.send_sms(
                user,
                'application_approved',
                application
            )
        
        Notification.objects.create(
            user=user,
            notification_type='Application_Approved',
            title='Application Approved!',
            message=f'Congratulations! Your application to {application.school.name} has been approved by the Ward Admin. Amount will be determined by CDF Office.'
        )
    
    @staticmethod
    def send_application_rejected_notification(application):
        """Send notification when application is rejected"""
        user = application.applicant
        preference = getattr(user, 'notification_preference', None)
        
        # Always send email on rejection (unless user explicitly disabled it)
        if not preference or preference.email_on_rejection:
            NotificationService.send_email(
                user,
                'application_rejected',
                application,
                context={'school': application.school.name, 'applicant_name': user.get_full_name()}
            )
        
        if preference and preference.sms_on_rejection:
            NotificationService.send_sms(
                user,
                'application_rejected',
                application
            )
        
        Notification.objects.create(
            user=user,
            notification_type='Application_Rejected',
            title='Application Status',
            message=f'Your application to {application.school.name} was not approved. Please check your email for the rejection reason.'
        )
    
    @staticmethod
    def send_email(user, template_type, application, context=None):
        """Send email using template"""
        try:
            template = EmailTemplateContentType.objects.get(
                template_type=template_type,
                is_active=True
            )
            
            subject = template.subject
            message = template.body
            
            # Replace variables
            if context:
                for key, value in context.items():
                    message = message.replace(f'{{{{{key}}}}}', str(value))
            
            # Get email from application or user
            email_address = application.email if application.email else user.email
            
            if not email_address:
                print(f"No email address found for user {user.username}")
                return
            
            email_notif = EmailNotification.objects.create(
                recipient=user,
                application=application,
                email_address=email_address,
                subject=subject,
                message=message,
                notification_type=template_type
            )
            
            # Send email
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email_address],
                fail_silently=False,
            )
            
            email_notif.status = 'Sent'
            email_notif.sent_date = timezone.now()
            email_notif.save()
            
            print(f"✓ Email sent to {email_address}: {subject}")
            
        except EmailTemplateContentType.DoesNotExist:
            print(f"Email template '{template_type}' not found. Please run: python manage.py populate_notification_templates")
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    @staticmethod
    def send_sms(user, template_type, application):
        """Send SMS notification"""
        try:
            # Get phone number from application first, then try user profile
            phone_number = None
            if application.phone_number:
                phone_number = application.phone_number
            elif hasattr(user, 'profile') and hasattr(user.profile, 'phone_number'):
                phone_number = user.profile.phone_number
            
            if not phone_number:
                print(f"No phone number found for user {user.username}")
                return
            
            template = SMSTemplate.objects.get(
                template_type=template_type,
                is_active=True
            )
            
            # Ensure phone number is in E.164 format
            if phone_number.startswith('0'):
                phone_number = '+254' + phone_number[1:]
            elif not phone_number.startswith('+'):
                phone_number = '+254' + phone_number
            
            sms_notif = SMSNotification.objects.create(
                recipient=user,
                application=application,
                phone_number=phone_number,
                message=template.message,
                notification_type=template_type
            )
            
            # Send SMS via Twilio
            if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=template.message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=phone_number
                )
                
                sms_notif.status = 'Sent'
                sms_notif.twilio_message_id = message.sid
                sms_notif.sent_date = timezone.now()
                print(f"✓ SMS sent to {phone_number}")
            else:
                sms_notif.status = 'Failed'
                sms_notif.error_message = 'Twilio credentials not configured'
                print(f"⚠ SMS not sent - Twilio credentials not configured. Would send to: {phone_number}")
                print(f"   Message: {template.message}")
            
            sms_notif.save()
            
        except SMSTemplate.DoesNotExist:
            print(f"SMS template '{template_type}' not found. Please run: python manage.py populate_notification_templates")
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
