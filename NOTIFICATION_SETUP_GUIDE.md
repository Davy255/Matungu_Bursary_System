# Email & SMS Notification Setup Guide

This guide will help you configure real email and SMS notifications for your Bursary Management System.

---

## 🔧 SETUP OVERVIEW

You have 3 configuration modes available:

1. **Console Mode** (Current) - Notifications print to terminal ✓ (Already working)
2. **Email Mode** - Real emails sent via Gmail 📧 (Setup below)
3. **SMS Mode** - Real SMS sent via Twilio 📱 (Setup below)

---

## 📧 PART 1: GMAIL EMAIL SETUP (5 minutes)

### Step 1: Enable 2-Factor Authentication

1. Open your browser and go to: https://myaccount.google.com/security
2. Sign in with: **davidwesonga776@gmail.com**
3. Scroll to "2-Step Verification"
4. If not enabled, click "Get Started" and follow the setup wizard
5. Verify with your phone number: **+254742669974**

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or search "App passwords" in Google Account settings
2. Under "Select app" dropdown → choose **Mail**
3. Under "Select device" dropdown → choose **Windows Computer**
4. Click **Generate**
5. Copy the 16-character password shown (format: `xxxx xxxx xxxx xxxx`)
   - Example: `abcd efgh ijkl mnop`

### Step 3: Update .env File

1. Open file: `Bursary_system\.env`
2. Find line with: `EMAIL_HOST_PASSWORD=PASTE_YOUR_16_CHAR_APP_PASSWORD_HERE`
3. Replace with your password (remove spaces):
   ```
   EMAIL_HOST_PASSWORD=abcdefghijklmnop
   ```
4. Save the file

### Step 4: Test Email

```powershell
# Restart Django server (press Ctrl+C in server terminal, then restart)
cd "c:\Users\user\Documents\Finalyearproject\Bursary_system"
.\venv\Scripts\python.exe manage.py runserver

# In a NEW terminal, test email:
.\venv\Scripts\python.exe manage.py test_notifications --type=submitted
```

✅ **Check your email inbox at davidwesonga776@gmail.com!**

---

## 📱 PART 2: TWILIO SMS SETUP (10 minutes)

### Step 1: Create Twilio Account (FREE)

1. Go to: https://www.twilio.com/try-twilio
2. Click **Sign up and start building**
3. Fill in the form:
   - First Name: **David**
   - Last Name: **Wesonga**
   - Email: **davidwesonga776@gmail.com**
   - Password: (create a strong password)
4. Click **Start your free trial**
5. Verify your email address (check inbox)
6. Verify your phone number: **+254742669974**
   - Enter the SMS code you receive

### Step 2: Get Free Trial Number

1. After login, you'll see the Twilio Console
2. Click **Get a Trial Number** button
3. Twilio will assign you a free phone number (e.g., `+1 234 567 8900`)
4. Click **Choose this Number**
5. **IMPORTANT:** Copy this number - you'll need it!

### Step 3: Get Your Credentials

1. In Twilio Console Dashboard, find:
   - **Account SID** (starts with "AC...")
     - Example: `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Auth Token** (click eye icon to reveal)
     - Example: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
2. **Copy both values**

### Step 4: Verify Your Phone Number (Important!)

During Twilio free trial, you can ONLY send SMS to verified numbers.

1. In Twilio Console, go to: **Phone Numbers** → **Verified Caller IDs**
2. Click **Add a new number** (+) button
3. Select **Kenya (+254)** as country
4. Enter: **742669974**
5. Click **Verify** via SMS
6. Enter the code you receive via SMS

### Step 5: Update .env File

Open `Bursary_system\.env` and update:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1234567890
```

Replace with YOUR actual values from Twilio Console.

### Step 6: Test SMS

```powershell
# Restart Django server
# Then test SMS:
.\venv\Scripts\python.exe manage.py test_notifications --type=submitted
```

✅ **Check your phone at +254742669974 for the SMS!**

---

## 🧪 TESTING ALL NOTIFICATIONS

Once configured, test all notification types:

### Test Application Submitted
```powershell
.\venv\Scripts\python.exe manage.py test_notifications --type=submitted
```

### Test Application Approved
```powershell
.\venv\Scripts\python.exe manage.py test_notifications --type=approved
```

### Test Application Rejected
```powershell
.\venv\Scripts\python.exe manage.py test_notifications --type=rejected
```

---

## ❓ TROUBLESHOOTING

### Email Not Sending?

1. **Check App Password**: Make sure you copied it correctly (no spaces)
2. **Check Gmail Settings**: Ensure 2FA is enabled
3. **Check Server Logs**: Look for error messages in terminal
4. **Try Another Email**: Test with a different Gmail account

### SMS Not Sending?

1. **Verify Phone Number**: Make sure +254742669974 is verified in Twilio
2. **Check Trial Balance**: Ensure you have trial credits left (check Twilio Console)
3. **Check Credentials**: Verify Account SID and Auth Token are correct
4. **Phone Format**: Ensure number is in E.164 format (+254...)

### Common Errors

**"Authentication failed"** - Wrong Gmail app password
**"Invalid credentials"** - Wrong Twilio Account SID or Auth Token
**"Unverified number"** - Phone number not verified in Twilio (trial limitation)

---

## 💰 COSTS

### Gmail (Email)
- ✅ **100% FREE** - Unlimited emails
- No charges ever

### Twilio (SMS)
- ✅ **$15 FREE Trial Credits**
- After trial: ~$0.05 per SMS (very cheap)
- Kenyan SMS to Safaricom: ~$0.07 per message
- You can add $20 credit for ~280 SMS messages

---

## 🔄 SWITCHING MODES

### Development Mode (Console only):
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Production Mode (Real emails):
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Gmail 2FA enabled
- [ ] Gmail App Password generated
- [ ] App password added to .env file
- [ ] Twilio account created
- [ ] Twilio phone number obtained
- [ ] Your phone (+254742669974) verified in Twilio
- [ ] Twilio credentials added to .env file
- [ ] Django server restarted
- [ ] Test email received in inbox
- [ ] Test SMS received on phone

---

## 🎉 SUCCESS!

Once all tests pass, your application will automatically send:
- ✅ Email notifications to applicants' email addresses
- ✅ SMS notifications to applicants' phone numbers

Notifications will trigger on:
1. Application submission
2. Application approval
3. Application rejection
4. Status updates

---

## 📞 NEED HELP?

If you get stuck, check:
1. Django server terminal for error messages
2. Gmail account security settings
3. Twilio Console logs (shows SMS delivery status)

Happy coding! 🚀
