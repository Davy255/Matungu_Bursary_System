import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 50)
print("EMAIL CONFIGURATION TEST")
print("=" * 50)
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else '(empty)'}")
print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
print("=" * 50)

# Try to send a test email
try:
    print("\nSending test email...")
    send_mail(
        subject='Test Email from Bursary System',
        message='This is a test email to verify email configuration.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['matungubursarysupportteam@gmail.com'],
        fail_silently=False,
    )
    print("✓ Email sent successfully!")
except Exception as e:
    print(f"✗ Error sending email: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
