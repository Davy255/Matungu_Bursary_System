# System Architecture

## High-Level Overview

The Matungu Bursary Management System is built on a **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│           (HTML Templates + Bootstrap + JavaScript)         │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Business Logic Layer                       │
│         (Django Views, Forms, Models, Services)             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   Data Access Layer                          │
│            (Django ORM, Database Queries)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  Database Layer                              │
│          (SQLite Dev / PostgreSQL Production)               │
└─────────────────────────────────────────────────────────────┘
```

## Django Application Structure

### Core Applications

#### 1. **users** - User Management
- User authentication and registration
- Profile management
- Role assignment (Super Admin, Ward Admin, CDF Admin)
- National ID verification
- User notifications

**Key Models:**
- `User` (Django built-in)
- `UserProfile` - Extended user info (phone, national ID, location)
- `AdminRole` - Administrative role assignment
- `Notification` - User notifications

**Key Views:**
- `register`, `login_view`, `profile_view`, `edit_profile`
- `password_reset`, `user_notifications`

#### 2. **applications** - Bursary Applications
- Application submission and tracking
- Multi-step application workflow (4 steps)
- Document upload and management
- Application status workflow
- Deadline management

**Key Models:**
- `Application` - Main application record
- `ApplicationDocument` - Uploaded documents
- `ApplicationApproval` - Approval records by different admins
- `Ward` - Geographic ward/constituency data
- `RegistrationSettings` - System-wide settings

**Key Views:**
- `new_application_step*` (1-4) - Multi-step form
- `application_detail`, `track_application`
- `applicant_dashboard`

#### 3. **admin_panel** - Administrative Functions
- Application review and approval workflow
- Applicant verification
- Award amount assignment
- Reports and analytics
- Admin role management

**Key Models:**
- `AdminApprovalLog` - Audit trail for approvals

**Key Views:**
- `admin_dashboard`, `applications_for_review`
- `approve_application`, `reject_application`
- `cdf_approved_applications`, `award_application_amount`
- `reports_dashboard`

#### 4. **schools** - Educational Institutions
- University management
- TVET college management
- Program management
- School data maintenance

**Key Models:**
- `School` - School information
- `Program` - Educational programs

#### 5. **notifications** - Notification System
- Email notifications
- SMS notifications (framework ready)
- Notification templates
- Notification preferences

**Key Models:**
- `NotificationTemplate` - Email templates
- `NotificationLog` - Sent notifications

#### 6. **bursary_system** - Core Configuration
- URL routing
- Settings management
- WSGI configuration

---

## Database Schema (Key Relationships)

```
┌─────────────────────┐
│   django_user       │
│ (Built-in Auth)     │
└──────────┬──────────┘
           │
           └─────────────┬──────────┬──────────┐
                         │          │          │
                    ┌────▼────┐ ┌──▼───┐ ┌───▼────┐
                    │UserProfile│AdminRole│Notification
                    └────┬────┘ └──────┘ └────────┘
                         │
                         │
                ┌────────┴──────────┐
                │                   │
           ┌────▼────┐        ┌────▼──────┐
           │Application    │ApplicationDocument
           └────────┘        └───────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼────┐   ┌──────▼─────┐
    │Ward     │   │ApplicationApproval
    └─────────┘   └────────────┘
```

---

## Data Flow

### Application Submission Flow

```
User Registration
    ↓
User Login
    ↓
Create Application (Step 1: School/Program Selection)
    ↓
Step 2: Personal Information + Ward Selection
    ↓
Step 3: Document Upload
    ↓
Step 4: Review & Submit
    ↓
Application Submitted → Status: "Submitted"
```

### Approval Workflow

```
Ward Admin Review
    ↓
  ┌─ Document Verification
  │     ↓
  └─→ Approve or Reject
        ↓
    If Rejected → Status: "Rejected"
        ↓
    If Approved → Status: "Approved" → ApplicationApproval created
                              ↓
                        CDF Admin Review
                              ↓
                         Award Amount
                              ↓
                        Status: "Amount Awarded"
```

---

## Authentication & Authorization

### User Roles

1. **Super Admin** (is_superuser=True)
   - Full system access
   - Manage all admins
   - View all data
   - Configuration management

2. **CDF Admin** (AdminRole.role_type='CDF_Admin')
   - Approve ward admin decisions
   - Award bursary amounts
   - View reports
   - Manage settings

3. **Ward Admin** (AdminRole.role_type='Ward_Admin')
   - Review applicant documents
   - Verify applicant information
   - Approve/reject applications
   - View ward-specific data

4. **Applicant** (User without admin role)
   - Submit application
   - Upload documents
   - Track application status
   - View own profile

### Permission Check Functions

```python
def is_admin(user):
    """Check if user is any type of admin"""
    
def get_admin_role_type(user):
    """Get admin type: Super_Admin, CDF_Admin, Ward_Admin"""
```

---

## Key Features

### 1. Multi-Step Application
- 4-step wizard interface
- Progress tracking
- Data persistence
- Validation at each step

### 2. Deadline Management
- Set application deadlines
- Countdown timer on dashboard
- Automated deadline enforcement
- Block submissions after deadline

### 3. Document Management
- Multiple document types
- File upload validation
- PDF generation
- Export functionality

### 4. Notification System
- Email notifications on status changes
- Admin notifications for new applications
- Template-based messages
- Audit trail

### 5. Reporting & Analytics
- Application statistics
- Ward-wise reports
- Award summaries
- Program distribution

---

## Technology Stack

### Backend
- **Framework:** Django 4.2
- **Database Driver:** psycopg2-binary (PostgreSQL)
- **Task Queue:** Celery 5.6.2
- **PDF Generation:** ReportLab 4.0.4

### Frontend
- **CSS Framework:** Bootstrap 5.3
- **Component Library:** Bootstrap Icons
- **JavaScript:** ES6+
- **Form Handling:** Django Crispy Forms

### DevOps & Tools
- **Environment:** Python 3.10+
- **Virtual Environment:** venv
- **Version Control:** Git
- **Database:** SQLite (dev), PostgreSQL (prod)

---

## Security Features

- ✅ CSRF Protection (Django built-in)
- ✅ SQL Injection Prevention (Django ORM)
- ✅ XSS Protection (Template auto-escaping)
- ✅ Password Hashing (Django built-in)
- ✅ National ID Fraud Detection
- ✅ Role-Based Access Control (RBAC)
- ✅ Session Management
- ✅ Email verification (optional)

---

## Performance Optimization

- **Database Indexing:** On frequently queried fields
- **Query Optimization:** select_related() and prefetch_related()
- **Caching:** Django cache framework ready
- **Pagination:** 20 items per page (configurable)
- **Static Files:** Minified CSS/JS via Bootstrap CDN

---

## Deployment Architecture

```
HTTP/HTTPS Request
        ↓
   Nginx/Apache
        ↓
   WSGI Server (Gunicorn)
        ↓
   Django Application
        ↓
   Celery Workers (Background tasks)
        ↓
   PostgreSQL Database
```

---

**For more details, see [Installation Guide](Installation-Guide.md) and [API Documentation](API-Documentation.md)**
