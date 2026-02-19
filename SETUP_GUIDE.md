# Bursary System - Setup Guide

## Quick Start Guide

This guide will help you get the Bursary Management System up and running on your development machine.

### System Requirements

- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **pip**: Latest version
- **Git**: For version control (optional)
- **RAM**: 2GB minimum
- **Disk Space**: 500MB

### Installation Steps

#### 1. Install Python and MySQL

**Windows:**
- Download Python from https://www.python.org/downloads/
- Download MySQL from https://dev.mysql.com/downloads/mysql/
- Follow installation wizards

**Mac:**
```bash
brew install python
brew install mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv mysql-server
```

#### 2. Create Project Directory

```bash
cd Documents
mkdir Bursary_system
cd Bursary_system
```

#### 3. Set Up Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

#### 5. Configure Database

**Create database in MySQL:**

```bash
mysql -u root -p

CREATE DATABASE bursary_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 6. Set Up Environment Variables

```bash
# Copy example to .env
cp .env.example .env

# Edit .env file with your credentials
```

**Edit `.bursary_system/settings.py`** for database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bursary_system',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

#### 7. Run Migrations

```bash
python manage.py migrate
```

You should see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

#### 8. Create Superuser Account

```bash
python manage.py createsuperuser
```

Follow the prompts to create admin account.

#### 9. Load Initial Data (Optional)

```bash
python manage.py populate_schools
```

This command adds sample schools to the database.

#### 10. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 11. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### Accessing the Application

- **Main Site**: http://localhost:8000
- **Admin Dashboard**: http://localhost:8000/admin
- **Superuser Login**: Use credentials created in step 8

### Troubleshooting

#### Issue: "No module named 'django'"

**Solution:**
```bash
pip install django==4.2.0
```

#### Issue: "Can't connect to MySQL server"

**Solution:**
- Ensure MySQL is running
- Check credentials in settings.py
- Verify database exists: `mysql -u root -e "SHOW DATABASES;"`

#### Issue: "Static files not loading"

**Solution:**
```bash
python manage.py collectstatic --clear --noinput
```

#### Issue: "Port 8000 already in use"

**Solution:**
```bash
python manage.py runserver 8001
```

### Creating Admin Accounts

#### Super Admin (via Django Admin)

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Click "Users" and create new user
4. Assign staff status and permissions

#### Ward Admin (via Management Command)

Create a custom management command or use Django shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from users.models import AdminRole

# Create user first
user = User.objects.create_user(
    username='ward_admin',
    email='wadmin@example.com',
    password='secure_password',
    first_name='Ward',
    last_name='Admin'
)

# Create admin role
admin_role = AdminRole.objects.create(
    user=user,
    role_type='Ward_Admin',
    ward='Matungu',
    assigned_by=User.objects.filter(is_superuser=True).first()
)

print("Ward admin created successfully")
exit()
```

### Database Backup

**Backup:**
```bash
mysqldump -u root -p bursary_system > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Restore:**
```bash
mysql -u root -p bursary_system < backup_file.sql
```

### Useful Django Commands

```bash
# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Run specific migration
python manage.py migrate app_name 0002

# Create superuser
python manage.py createsuperuser

# Run management command
python manage.py populate_schools

# Access database shell
python manage.py shell

# Run tests
python manage.py test

# Clear old migrations
python manage.py migrate app_name zero

# Generate secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Email Configuration

For Gmail:
1. Enable "Less Secure App Access": https://myaccount.google.com/lesssecureapps
2. Use app-specific password if 2FA is enabled
3. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

### SMS Configuration (Twilio)

1. Create Twilio account: https://www.twilio.com
2. Get Account SID, Auth Token, and SMS number
3. Add to `.env`:
   ```
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

### Testing the System

#### Test Application Submission Flow

1. Register as new applicant
2. Create new application
3. Select school and program
4. Fill application form
5. Upload documents
6. Submit application
7. Login as admin to review

#### Test Email Notifications

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test message',
    'from@example.com',
    ['to@example.com'],
)
```

### Performance Optimization

- Add caching with Redis
- Use Celery for async tasks
- Enable database query optimization
- Minify static files
- Use CDN for static assets

### Security Checklist for Production

- [ ] Change DEBUG to False
- [ ] Generate strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS
- [ ] Set up SSL certificate
- [ ] Configure secure cookies
- [ ] Enable CSRF protection
- [ ] Set up rate limiting
- [ ] Regular security updates
- [ ] Database backups
- [ ] Monitor error logs

### Deployment Checklist

- [ ] All migrations applied
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Database backups set up
- [ ] Email configured
- [ ] SMS configured
- [ ] Security settings updated
- [ ] Logging configured
- [ ] Error monitoring set up

### Support
For additional help, refer to:
- Django Documentation: https://docs.djangoproject.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Bootstrap Documentation: https://getbootstrap.com/docs/

---

**Last Updated**: February 2024
