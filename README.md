# Bursary Management System

A comprehensive web application for managing bursary applications, built with Django 6.0 and MySQL.

## 🚀 Features Implemented

### ✅ Complete System
All functionality has been built and is working:

#### User Management
- **User Registration** - Students can create accounts
- **User Login/Logout** - Secure authentication system
- **User Profiles** - Extended profile with personal information (ID, guardian details, location)
- **Custom User Model** - Extended Django's User with roles (student, admin, reviewer)

#### Bursary Applications
- **Application Creation** - Students can apply for bursaries
- **Document Upload** - Support for multiple document types (ID, admission letter, fee structure, etc.)
- **Application Tracking** - View all applications with status (draft, submitted, under review, approved, rejected)
- **Application Submission** - Convert draft to submitted application
- **Status Management** - Track application through entire lifecycle

#### Schools & Programs
- **School Database** - Universities, colleges, TVET institutions, polytechnics
- **Campus Management** - Multiple campuses per school
- **Program Management** - Academic programs with levels (certificate, diploma, degree, masters, PhD)
- **School Search** - Search by name and filter by type

#### Admin Dashboard
- **Django Admin Panel** - Full CRUD operations for all models
- **Application Review System** - Reviewers can score and recommend applications
- **Application Approval** - Approvers can set approved amounts and disbursement details
- **Notifications** - System for notifying users of application status changes

## 📊 Database Schema

**12 Tables Created:**
1. **User** - Custom user model with roles
2. **UserProfile** - Extended user information
3. **AdminRole** - Admin-specific permissions
4. **PasswordReset** - Password reset tokens
5. **School** - Educational institutions
6. **Campus** - School branches
7. **Program** - Academic programs
8. **Ward** - Administrative wards
9. **Application** - Bursary applications
10. **ApplicationDocument** - Uploaded documents
11. **ApplicationReview** - Review records
12. **ApplicationApproval** - Approval records
13. **Notification** - User notifications

## 🗄️ Technology Stack

- **Backend**: Django 6.0.3
- **Database**: MySQL 8.x
- **Database Driver**: PyMySQL 1.1.1
- **Image Processing**: Pillow 12.1.1
- **Configuration**: python-decouple 3.8

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.14.0
- MySQL Server 8.x
- Virtual environment activated

### Database Configuration
Database credentials are stored in `.env`:
```
DB_NAME=bursary_db
DB_USER=bursary_app
DB_PASSWORD=@David2211.
DB_HOST=localhost
DB_PORT=3306
DB_ENGINE=django.db.backends.mysql
```

### Running the Application

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

3. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Populate sample data** (optional):
   ```bash
   python manage.py populate_sample_data
   ```
   This adds:
   - 3 wards (Matungu, Koyonzo, Kholera)
   - 3 schools (UON, MMUST, KMTC)
   - 6 programs across different levels

## 📁 Project Structure

```
Bursary_system/
├── config/                  # Project settings
│   ├── settings.py         # Main configuration (MySQL, custom User)
│   ├── urls.py             # URL routing
│   └── __init__.py         # PyMySQL compatibility layer
├── users/                   # User management app
│   ├── models.py           # User, UserProfile, AdminRole, PasswordReset
│   ├── views.py            # Registration, login, profile, dashboard
│   ├── forms.py            # Registration, login, profile forms
│   ├── admin.py            # Admin configuration
│   └── templates/          # HTML templates
├── applications/            # Bursary applications app
│   ├── models.py           # Application, Document, Review, Approval, Ward
│   ├── views.py            # Apply, upload, submit, view applications
│   ├── forms.py            # Application and document upload forms
│   ├── admin.py            # Admin configuration
│   └── templates/          # HTML templates
├── schools/                 # Schools management app
│   ├── models.py           # School, Campus, Program
│   ├── admin.py            # Admin configuration
│   └── management/commands/
│       └── populate_sample_data.py  # Sample data loader
├── notifications/           # Notifications app
│   ├── models.py           # Notification
│   └── admin.py            # Admin configuration
├── admin_panel/             # Admin-specific features (ready for expansion)
├── media/                   # Uploaded files (documents, photos)
├── staticfiles/            # Static files (CSS, JS, images)
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration (not in git)
```

## 🌐 Available URLs

### Public Pages
- `/` - Homepage
- `/register/` - User registration
- `/login/` - User login

### Authenticated Pages  
- `/dashboard/` - User dashboard
- `/profile/` - User profile edit
- `/applications/apply/` - Create new application
- `/applications/my-applications/` - View all user applications
- `/applications/<id>/` - View single application
- `/applications/<id>/upload/` - Upload documents
- `/applications/<id>/submit/` - Submit application
- `/applications/schools/` - Search schools

### Admin Pages
- `/admin/` - Django admin panel (full CRUD access)

## 🎯 User Workflow

1. **Student Registration**
   - Register account → Complete profile → Ready to apply

2. **Bursary Application**
   - Create application → Fill details (school, program, finances)
   - Upload documents (ID, admission letter, fee structure)
   - Submit for review

3. **Application Review** (Admin)
   - Review application in admin panel
   - Add review with score and recommendation
   - Approve/reject application

4. **Disbursement** (Finance)
   - Set approved amount
   - Record disbursement date and reference

## ✨ Key Features

- **Custom User Model** with email as unique identifier
- **Role-based Access** (student, admin, reviewer)
- **Document Management** with file size validation (5MB limit)
- **Multi-step Application** process (draft → submit → review → approve)
- **School Search** with filtering by type
- **Admin Dashboard** with all CRUD operations
- **Responsive Design** with clean, modern UI
- **MySQL Integration** with proper foreign keys and relationships

## 🔒 Security Features

- Password hashing and validation
- CSRF protection on all forms
- Login required decorators
- User-specific data access (students can only see their own applications)
- Environment-based configuration (.env file)

## 📝 Sample Data Included

Run `python manage.py populate_sample_data` to add:
- **3 Wards**: Matungu, Koyonzo, Kholera (Kakamega County)
- **3 Schools**: University of Nairobi, MMUST, KMTC
- **6 Programs**: CS, Medicine, Education, IT, Clinical Medicine, Community Health

## 🚧 Ready for Expansion

The system is fully functional and ready for:
- Email notifications
- Payment integration
- Reporting and analytics
- Application scoring algorithms
- Bulk operations
- Export to PDF/Excel
- SMS notifications

## 📞 Support

All models are registered in the admin panel for easy management. Create a superuser account to access full administrative features.

---

**Status**: ✅ Fully Implemented and Working
**Database**: ✅ MySQL with all tables created
**Authentication**: ✅ Complete with registration and login
**Applications**: ✅ Full workflow from creation to approval
**Admin**: ✅ Django admin panel configured
