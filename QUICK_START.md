# Quick Start Checklist

Use this checklist to quickly get the Bursary System up and running.

## Pre-Installation (5 minutes)
- [ ] Download and install Python 3.8+
- [ ] Download and install MySQL Server
- [ ] Download and install Git (optional)
- [ ] Create project folder
- [ ] Open terminal/command prompt

## Installation (15-20 minutes)
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` with your credentials

## Database Setup (10 minutes)
- [ ] Start MySQL Server
- [ ] Create database: `CREATE DATABASE bursary_system;`
- [ ] Update database credentials in `settings.py`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Verify migrations: Check Django admin tables created

## Initial Setup (10 minutes)
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Load schools data: `python manage.py populate_schools` (optional)
- [ ] Collect static files: `python manage.py collectstatic --noinput`

## Testing (5 minutes)
- [ ] Start server: `python manage.py runserver`
- [ ] Visit `http://localhost:8000` - Should see error (no template yet)
- [ ] Visit `http://localhost:8000/admin` - Should see login
- [ ] Login with superuser credentials
- [ ] Verify can see Django admin

## First Applicant Setup (15 minutes)
- [ ] Create new user (applicant) in admin
- [ ] Logout and login as new user
- [ ] Visit dashboard (should work with base template)
- [ ] Try to create new application
- [ ] Select school and proceed
- [ ] Fill application form
- [ ] Upload a test document
- [ ] Submit application

## First Admin Setup (10 minutes)
- [ ] Create new user in admin as staff
- [ ] Create AdminRole for that user
- [ ] Assign to Ward Admin role
- [ ] Assign to 'Matungu' ward
- [ ] Logout and login as admin
- [ ] Visit admin dashboard
- [ ] View pending applications
- [ ] Approve/reject an application

## Email Setup (10 minutes)
- [ ] Set up Gmail account (or use SendGrid)
- [ ] Enable "Less Secure Apps" on Gmail
- [ ] Add email credentials to `.env`
- [ ] Test email: `python manage.py shell`
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
  ```
- [ ] Verify email received

## SMS Setup (Optional - 10 minutes)
- [ ] Create Twilio account
- [ ] Get Account SID, Auth Token, Phone Number
- [ ] Add to `.env`
- [ ] Update notification templates in admin
- [ ] Test SMS (requires valid phone)

## Final Checks (10 minutes)
- [ ] Test user registration
- [ ] Test user login
- [ ] Test application workflow (all 4 steps)
- [ ] Test document upload
- [ ] Test admin review workflow
- [ ] Test notifications
- [ ] Test export functions
- [ ] Test error handling

## Deployment Preparation (Optional)
- [ ] Read DEPLOYMENT_GUIDE.md
- [ ] Generate secure SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL certificate
- [ ] Configure firewall
- [ ] Set up database backups

## Common Issues & Solutions

### Virtual Environment Won't Activate
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### MySQL Connection Error
- Verify MySQL is running: `mysql -u root -p`
- Check credentials in `settings.py`
- Verify database exists: `SHOW DATABASES;`

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Dependencies Not Installing
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Templates Not Found
- Verify `templates/` directory exists
- Check `TEMPLATES` in `settings.py`
- Run `python manage.py collectstatic`

## Next Steps After Installation

1. **Customize Templates**
   - Update branding/colors
   - Add custom CSS
   - Modify page layouts

2. **Configure Email Templates**
   - Go to admin panel
   - Create email templates
   - Customize messages

3. **Load School Data**
   - Run populate_schools command
   - Or manually add via admin panel
   - Add campuses and programs

4. **Set Up Admin Accounts**
   - Create ward admins
   - Create CDF admins
   - Test approval workflows

5. **Test Full Workflow**
   - Register multiple applicants
   - Submit applications
   - Review and approve
   - Check notifications

## Useful Django Commands

```bash
# Database
python manage.py migrate
python manage.py makemigrations
python manage.py sqlmigrate app_name 0001

# Users
python manage.py createsuperuser
python manage.py changepassword username

# Data
python manage.py populate_schools
python manage.py shell
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Files
python manage.py collectstatic
python manage.py clearsessions

# Testing
python manage.py test
python manage.py test app_name
python manage.py test app_name.tests.TestClass
```

## Environment Variables Reference

```
DEBUG=True/False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=bursary_system
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=app-password

TWILIO_ACCOUNT_SID=sid
TWILIO_AUTH_TOKEN=token
TWILIO_PHONE_NUMBER=+1234567890
```

## Support Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django Rest Framework**: https://www.django-rest-framework.org/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Python Documentation**: https://docs.python.org/

## Getting Help

If you encounter issues:

1. **Check logs**: Look at console output and Django error pages
2. **Google the error**: Most errors have solutions online
3. **Check Django docs**: Comprehensive documentation available
4. **Review code comments**: Many solutions are commented in code
5. **Ask on Stack Overflow**: Tag with django, python, mysql

---

## Estimated Setup Time

- **Total Setup Time**: 60-90 minutes (first time)
- **Subsequent Setups**: 20-30 minutes (with experience)
- **Installation Only**: 15-20 minutes

## Success Indicators

You've successfully set up the system when:

✓ Can access Django admin panel
✓ Can register new user
✓ Can create application as applicant
✓ Can login as admin and view applications
✓ Can approve/reject applications
✓ Can receive email notifications
✓ Can export approved applicants

---

**Last Updated**: February 2024
