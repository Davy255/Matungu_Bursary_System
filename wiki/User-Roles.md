# User Roles

## System Role Hierarchy

```
┌─────────────────────────────────────────┐
│         SUPER ADMIN                     │
│  (System-wide access)                   │
│  is_superuser=True                      │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
    ┌───▼────────┐   ┌──────▼─────┐
    │ CDF ADMIN  │   │ WARD ADMIN  │
    │ (County)   │   │ (Ward)      │
    └──────┬─────┘   └─────┬───────┘
           │               │
           └───────┬───────┘
                   │
             ┌─────▼─────┐
             │ APPLICANT  │
             └────────────┘
```

---

## Role Permissions Matrix

| Feature | Super Admin | CDF Admin | Ward Admin | Applicant |
|---------|:----------:|:----------:|:----------:|:----------:|
| View All Applications | ✅ | ✅ | ⚠️ (Ward only) | ❌ |
| Approve Applications | ✅ | ✅ | ✅ | ❌ |
| Award Amounts | ✅ | ✅ | ❌ | ❌ |
| Verify Applicants | ✅ | ❌ | ✅ | ❌ |
| Manage Admins | ✅ | ❌ | ❌ | ❌ |
| View Reports | ✅ | ✅ | ⚠️ (Ward) | ❌ |
| Submit Application | ❌ | ❌ | ❌ | ✅ |
| Track Application | ⚠️ (All) | ❌ | ❌ | ✅ (Own) |
| Edit Profile | ✅ | ✅ | ✅ | ✅ |
| Manage Settings | ✅ | ✅ | ❌ | ❌ |

---

## Role Descriptions

### 1. Super Admin (System Administrator)

**Identification:**
- Django `is_superuser=True`
- No `AdminRole` object needed
- Can access all system functions

**Responsibilities:**
- Manage all user accounts
- Assign admin roles
- Configure system settings
- View system-wide reports
- Monitor application deadlines
- Handle escalations

**Dashboard Access:**
- Full admin dashboard
- All applications visible
- System statistics
- No location information required

**Key Permissions:**
```python
User.is_superuser = True
# No AdminRole needed
```

---

### 2. CDF Admin (County Development Fund Administrator)

**Identification:**
- `AdminRole.role_type = 'CDF_Admin'`
- `AdminRole.scope = 'county'`

**Responsibilities:**
- Review ward admin approvals
- Award final bursary amounts
- Approve/reject applications
- Manage CDF fund allocation
- Track award statistics
- Generate county-level reports

**Dashboard Access:**
- CDF-specific dashboard
- Ward-approved applications
- Award management interface
- County statistics

**Key Actions:**
- `cdf_approved_applications` - View ready-to-award applications
- `award_application_amount` - Assign bursary amount
- `export_approved_applicants` - Generate reports

**Database Model:**
```python
AdminRole(
    role_type='CDF_Admin',
    scope='county'
)
```

---

### 3. Ward Admin (Ward-Level Administrator)

**Identification:**
- `AdminRole.role_type = 'Ward_Admin'`
- `AdminRole.scope = 'ward'`
- `AdminRole.ward = 'Ward_Name'`

**Responsibilities:**
- Review applicant documents
- Verify personal information
- Investigate fraud claims
- Approve/reject applications
- Provide recommendations
- Handle local escalations

**Dashboard Access:**
- Ward-specific dashboard
- Ward applications only
- Ward statistics
- Applicant detail pages

**Key Actions:**
- `applications_for_review` - Pending applications
- `approve_application` - Approve with comments
- `reject_application` - Reject with reason
- `manage_verifications` - Handle fraud reports

**Database Model:**
```python
AdminRole(
    role_type='Ward_Admin',
    scope='ward',
    ward='Mayoni'  # or other wards
)
```

**Ward List:**
- Mayoni
- Kholera
- Khalaba
- Koyonzo
- Namamali

---

### 4. Applicant (Regular User)

**Identification:**
- Regular Django user
- No admin roles
- `UserProfile.user_type = 'Applicant'`

**Responsibilities:**
- Submit bursary applications
- Upload required documents
- Provide accurate information
- Monitor application progress

**Access:**
- Personal dashboard
- Application submission
- Document upload
- Application tracking
- Profile management

**Key Actions:**
- `new_application_step1-4` - Submit application
- `applicant_dashboard` - View own applications
- `track_application` - Monitor progress
- `upload_documents` - Upload support documents

**Constraints:**
- Cannot access admin panel
- Cannot see other applications
- Cannot approve/reject
- Deadline blocking (cannot submit after deadline)

---

## Role Assignment Process

### For Admins

**Super Admin Method (Direct):**
```python
# Create superuser via command
python manage.py createsuperuser

# Or via admin panel
# Navigate to: /admin/auth/user/
```

**Ward/CDF Admin Method (AdminRole):**

1. Go to Admin Panel → Manage Admins
2. Click "Assign New Admin Role"
3. Select user
4. Choose role type:
   - **Ward Admin** → Select ward
   - **CDF Admin** → No location needed
5. Assign created by superuser: `approval_level='Super_Admin'`
6. Admin role is created

```python
AdminRole.objects.create(
    user=user_obj,
    role_type='Ward_Admin',
    ward='Mayoni',
    assigned_by=superuser,
    is_verified=True
)
```

---

## Permission Checking

### Helper Functions

```python
def is_admin(user):
    """Check if user is any type of admin"""
    if user.is_superuser:
        return True
    if user.is_staff and hasattr(user, 'admin_role'):
        return True
    return False

def get_admin_role_type(user):
    """Safely get admin type"""
    if user.is_superuser:
        return 'Super_Admin'
    try:
        if hasattr(user, 'admin_role') and user.admin_role:
            return user.admin_role.role_type
    except:
        pass
    return 'Super_Admin'
```

### Permission Decorators

```python
@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('access_denied')
    
    admin_type = get_admin_role_type(request.user)
    # ... admin logic

@login_required
def cdf_function(request):
    if get_admin_role_type(request.user) != 'CDF_Admin':
        return redirect('access_denied')
    # ... CDF-specific logic
```

---

## Workflow by Role

### Application Lifecycle

```
APPLICANT
  ├─ Register/Login
  ├─ Create Application (Steps 1-4)
  ├─ Upload Documents
  └─ Submit Application
          ↓
WARD ADMIN
  ├─ Receive Notification
  ├─ Review Documents
  ├─ Verify Information
  └─ Approve/Reject
          ↓
       (If Approved)
          ↓
CDF ADMIN
  ├─ Review Decision
  ├─ Award Amount
  └─ Approve Amount
          ↓
APPLICANT
  └─ Receive Notification & Award Info
          ↓
SUPER ADMIN
  └─ Monitor & Generate Reports
```

---

## User Profile Visibility

| Field | Super Admin | Ward Admin | CDF Admin | Applicant |
|-------|:----------:|:----------:|:----------:|:----------:|
| Location (Ward/County) | Hidden | Visible | Visible | Visible |
| National ID | Visible | Visible | Visible | Own only |
| Phone Number | Visible | Visible | Visible | Own only |
| Email | Visible | Visible | Visible | Own only |
| Admin Role | Visible | Visible | Visible | N/A |

---

## Security Notes

- Super Admins have no location restrictions
- Ward Admins see data only for their assigned ward
- CDF Admins see county-wide data
- All role changes logged for audit trail
- Role verification required for sensitive operations
- Password reset available for all roles

---

**See also:** [Admin Guide](Admin-Guide.md), [Getting Started](User-Guide.md)
