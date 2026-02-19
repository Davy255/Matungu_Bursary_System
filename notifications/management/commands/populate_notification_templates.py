from django.core.management.base import BaseCommand
from notifications.models import EmailTemplateContentType, SMSTemplate


class Command(BaseCommand):
    help = 'Populate notification templates for email and SMS'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating notification templates...')
        
        # Email Templates
        email_templates = [
            {
                'template_type': 'application_submitted',
                'subject': 'Application Submitted Successfully',
                'body': '''Dear Applicant,

Your bursary application to {{school}} has been submitted successfully.

Application Details:
- School: {{school}}
- Submission Date: Today

What's Next?
Your application will be reviewed by our team. We'll notify you once a decision has been made.

Thank you for applying!

Best regards,
Matungu Subcounty Bursary Committee''',
                'is_active': True
            },
            {
                'template_type': 'application_approved',
                'subject': 'Congratulations! Your Application Has Been Approved',
                'body': '''Dear Applicant,

Congratulations! We are pleased to inform you that your bursary application to {{school}} has been APPROVED.

Next Steps:
1. Check your application details in your dashboard
2. Wait for further instructions from the school
3. Prepare required documentation

We wish you success in your studies!

Best regards,
Matungu Subcounty Bursary Committee''',
                'is_active': True
            },
            {
                'template_type': 'application_rejected',
                'subject': 'Bursary Application Status Update',
                'body': '''Dear Applicant,

Thank you for your interest in the Matungu Subcounty Bursary Program.

After careful consideration, we regret to inform you that your application to {{school}} was not approved at this time.

You can:
- View feedback in your application details
- Apply to other schools
- Reapply in the next cycle

We encourage you to explore other funding opportunities.

Best regards,
Matungu Subcounty Bursary Committee''',
                'is_active': True
            },
            {
                'template_type': 'application_update',
                'subject': 'Application Status Update',
                'body': '''Dear Applicant,

There has been an update to your bursary application to {{school}}.

Please log in to your account to view the details.

Best regards,
Matungu Subcounty Bursary Committee''',
                'is_active': True
            },
        ]
        
        for template_data in email_templates:
            template, created = EmailTemplateContentType.objects.update_or_create(
                template_type=template_data['template_type'],
                defaults={
                    'subject': template_data['subject'],
                    'body': template_data['body'],
                    'is_active': template_data['is_active']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created email template: {template.template_type}'))
            else:
                self.stdout.write(self.style.WARNING(f'→ Updated email template: {template.template_type}'))
        
        # SMS Templates
        sms_templates = [
            {
                'template_type': 'application_submitted',
                'message': 'Your bursary application has been submitted successfully. We will review it and notify you of the outcome. - Matungu Bursary',
                'is_active': True
            },
            {
                'template_type': 'application_approved',
                'message': 'Congratulations! Your bursary application has been APPROVED. Check your email for details. - Matungu Bursary',
                'is_active': True
            },
            {
                'template_type': 'application_rejected',
                'message': 'Your bursary application was not approved. Please check your email for details and feedback. - Matungu Bursary',
                'is_active': True
            },
            {
                'template_type': 'application_update',
                'message': 'Your bursary application has been updated. Log in to view details. - Matungu Bursary',
                'is_active': True
            },
        ]
        
        for template_data in sms_templates:
            template, created = SMSTemplate.objects.update_or_create(
                template_type=template_data['template_type'],
                defaults={
                    'message': template_data['message'],
                    'is_active': template_data['is_active']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created SMS template: {template.template_type}'))
            else:
                self.stdout.write(self.style.WARNING(f'→ Updated SMS template: {template.template_type}'))
        
        self.stdout.write(self.style.SUCCESS('\n✅ All notification templates created successfully!'))
