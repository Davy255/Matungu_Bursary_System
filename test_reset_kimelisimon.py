import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from users.models import User, PasswordReset
from django.utils import timezone
from datetime import timedelta
import random
import string

try:
    print("=" * 60)
    print("TESTING PASSWORD RESET FOR: kimelisimon27@gmail.com")
    print("=" * 60)
    
    # Get user
    user = User.objects.get(email='kimelisimon27@gmail.com')
    print(f"✓ User found: {user.username}")
    
    # Generate code
    code = ''.join(random.choices(string.digits, k=6))
    print(f"✓ Code generated: {code}")
    
    # Create reset token
    reset_token = PasswordReset.objects.create(
        user=user,
        token=code,
        expires_at=timezone.now() + timedelta(hours=1),
        is_used=False
    )
    print(f"✓ Reset token created in database")
    
    # Send email
    print(f"\nSending email to {user.email}...")
    send_mail(
        subject='Password Reset Code for Bursary System',
        message=f'Your password reset code is: {code}\n\nThis code will expire in 1 hour.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    
    print(f"✓ Email sent successfully!")
    print(f"\n✓ Password reset code: {code}")
    print(f"✓ Check kimelisimon27@gmail.com inbox for the email")
    
except User.DoesNotExist:
    print("✗ User not found")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
