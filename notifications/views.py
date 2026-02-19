from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import EmailNotification, SMSNotification, NotificationPreference


@login_required
def notification_preferences(request):
    """View and edit notification preferences"""
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preference.email_on_submission = request.POST.get('email_on_submission') == 'on'
        preference.email_on_approval = request.POST.get('email_on_approval') == 'on'
        preference.email_on_rejection = request.POST.get('email_on_rejection') == 'on'
        preference.email_on_comment = request.POST.get('email_on_comment') == 'on'
        preference.email_on_update = request.POST.get('email_on_update') == 'on'
        
        preference.sms_on_submission = request.POST.get('sms_on_submission') == 'on'
        preference.sms_on_approval = request.POST.get('sms_on_approval') == 'on'
        preference.sms_on_rejection = request.POST.get('sms_on_rejection') == 'on'
        preference.sms_on_update = request.POST.get('sms_on_update') == 'on'
        
        preference.save()
        
        from django.contrib import messages
        messages.success(request, 'Your preferences have been updated.')
        return render(request, 'notifications/preferences.html', {'preference': preference})
    
    return render(request, 'notifications/preferences.html', {'preference': preference})
