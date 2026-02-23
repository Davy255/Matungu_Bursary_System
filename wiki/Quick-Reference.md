# Quick Reference Guide

## Command Cheat Sheet

### Virtual Environment
```bash
# Create
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Deactivate
deactivate
```

### Installation & Setup
```bash
# Install packages
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create super user
python manage.py createsuperuser

# Load sample data
python manage.py populate_universities
python manage.py populate_tvets
python manage.py populate_schools
python manage.py populate_wards
python manage.py populate_notification_templates
```

### Development Server
```bash
# Run server
python manage.py runserver

# Run on specific port
python manage.py runserver 8001

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000

# Stop server
Ctrl+C
```

### Database
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reset migrations (development only!)
python manage.py migrate zero
python manage.py migrate

# Database shell
python manage.py dbshell

# Backup
cp db.sqlite3 backup.sqlite3
```

### Django Admin
```bash
# Access
http://localhost:8000/admin

# Check system
python manage.py check

# Collect static files
python manage.py collectstatic

# Clear cache
python manage.py clear_cache
```

### Testing
```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test applications

# Run with verbosity
python manage.py test --verbosity=2
```

---

## URL Quick Links

| Page | URL |
|------|-----|
| Home | `/` |
| Login | `/login/` |
| Register | `/register/` |
| Dashboard | `/dashboard/` |
| Profile | `/profile/` |
| Edit Profile | `/profile/edit/` |
| New Application S1 | `/applications/new/` |
| New Application S2 | `/applications/<id>/step2/` |
| New Application S3 | `/applications/<id>/step3/` |
| New Application S4 | `/applications/<id>/step4/` |
| Application Detail | `/applications/<id>/` |
| Track Application | `/applications/track/` |
| Admin Dashboard | `/admin-panel/dashboard/` |
| Applications for Review | `/admin-panel/applications-for-review/` |
| Approve Application | `/admin-panel/approve/<id>/` |
| CDF Applications | `/admin-panel/cdf-applications/` |
| Award Amount | `/admin-panel/award/<id>/` |
| Reports | `/admin-panel/reports/` |
| Django Admin | `/admin/` |
| Admin API | `/api/` |

---

## Model Quick Reference

### User Models
```python
# Original Django User
User
  ├── username
  ├── email
  ├── password
  └── is_superuser

# Extended Profile
UserProfile
  ├── phone_number
  ├── national_id
  ├── county
  ├── ward
  ├── user_type
  └── is_verified

# Admin Role
AdminRole
  ├── user (FK)
  ├── role_type (CDF_Admin, Ward_Admin)
  ├── ward (if Ward_Admin)
  └── assigned_by (Super Admin)
```

### Application Models
```python
Application
  ├── applicant (FK to User)
  ├── school (FK to School)
  ├── program (FK to Program)
  ├── status (Draft, Submitted, etc.)
  ├── date_of_birth
  ├── national_id
  ├── phone_number
  ├── gender
  ├── ward (FK to Ward)
  └── submitted_date

ApplicationDocument
  ├── application (FK)
  ├── document (FileField)
  ├── document_type
  └── upload_date

ApplicationApproval
  ├── application (FK)
  ├── approved_by (FK to User)
  ├── approval_level
  ├── status
  ├── amount_approved
  └── approved_date
```

### Supporting Models
```python
School
  ├── name
  ├── school_type
  ├── location
  └── is_active

Program
  ├── school (FK)
  ├── name
  ├── level
  └── is_available

Ward
  ├── name
  ├── constituency
  ├── county
  └── is_active
```

---

## Important Environment Variables

```bash
# Django
DEBUG=True|False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3
# or
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Files
MEDIA_URL=/media/
MEDIA_ROOT=media/
STATIC_URL=/static/
STATIC_ROOT=staticfiles/

# Security
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True (production)
SESSION_COOKIE_SECURE=True (production)
```

---

## Django Settings Locations

```
bursary_system/
├── settings.py          # Main settings file
├── urls.py              # URL routing
├── wsgi.py              # WSGI configuration
└── requirements.txt     # Package dependencies
```

---

## Common Errors & Quick Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: django` | `pip install -r requirements.txt` |
| `Port 8000 in use` | `python manage.py runserver 8001` |
| `Database locked` | Close other terminals, restart server |
| `Static files not found` | `python manage.py collectstatic` |
| `No migrations` | `python manage.py makemigrations` |
| `Migration conflicts` | `python manage.py migrate zero && migrate` |
| `Permission denied` | Run with admin user/superuser |

---

## Permission Checks

```python
# Check if admin
from admin_panel.views import is_admin
if is_admin(request.user):
    # Admin logic

# Get admin type
from admin_panel.views import get_admin_role_type
role = get_admin_role_type(request.user)
if role == 'Super_Admin':
    # Super admin
elif role == 'CDF_Admin':
    # CDF logic
elif role == 'Ward_Admin':
    # Ward logic
```

---

## File Structure Essentials

```
Bursary_system/
├── admin_panel/              # Admin interface app
│   ├── views.py             # Admin logic
│   ├── models.py            # Related models
│   ├── urls.py              # Admin URLs
│   └── templates/
│
├── applications/            # Application app
│   ├── views.py            # Application logic
│   ├── models.py           # Application models
│   ├── forms.py            # Application forms
│   └── templates/
│
├── users/                   # User management
│   ├── views.py            # User views
│   ├── models.py           # User models
│   ├── forms.py            # User forms
│   └── templates/
│
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── users/              # User templates
│   ├── applications/       # App templates
│   └── admin_panel/        # Admin templates
│
├── static/                  # CSS, JS, images
│   └── css/style.css
│
├── db.sqlite3              # Development database
├── manage.py               # Django management
├── requirements.txt        # Dependencies
└── wiki/                   # This documentation!
```

---

## Key Passwords & Credentials

### For Testing
Use during development:
```
Username: testadmin
Password: TestPassword123!

Username: testuser
Password: TestPassword123!
```

### Production Security
- Use strong SECRET_KEY
- Set DEBUG=False
- Use environment variables
- Secure database credentials
- HTTPS enabled
- Regular backups

---

## Git Commands

```bash
# Check status
git status

# Add changes
git add -A

# Commit
git commit -m "Meaningful message"

# Push to GitHub
git push origin main

# Pull latest
git pull origin main

# View history
git log --oneline -5

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main
```

---

## Support Resources

- 📖 **Wiki:** [Home](Home.md)
- 📚 **Django:** [docs.djangoproject.com](https://docs.djangoproject.com)
- 🆘 **Issues:** GitHub Issues
- 📧 **Contact:** Admin email

---

## Useful Commands by Role

### Super Admin
```bash
python manage.py createsuperuser  # Create admin user
python manage.py check            # System check
python manage.py dbshell          # Database access
```

### Developer
```bash
python manage.py makemigrations   # Create migrations
python manage.py migrate          # Apply migrations
python manage.py test             # Run tests
python manage.py runserver        # Development server
```

### DevOps
```bash
python manage.py collectstatic    # Production static files
sudo systemctl restart gunicorn  # Restart production server
pg_dump dbname > backup.sql      # Database backup
```

---

**Last Updated:** February 24, 2026  
**Version:** 1.0
