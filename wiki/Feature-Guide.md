# Feature Guide

## Overview of Key Features

This guide details the main features of the Matungu Bursary Management System as of February 2026.

---

## 1. Password Visibility Toggle

### What It Does
Users can click an eye icon to reveal/hide their password while typing.

### Where It's Available
- **Login Page** - Both username and password fields
- **Register Page** - Both password and confirm password fields

### How It Works

**HTML Template:**
```html
<div class="input-group">
    <input type="password" id="password" name="password" class="form-control">
    <button type="button" class="btn btn-outline-secondary" id="togglePassword">
        <i class="fa fa-eye"></i>
    </button>
</div>
```

**JavaScript Implementation:**
```javascript
document.getElementById('togglePassword').addEventListener('click', function() {
    const input = document.getElementById('password');
    const icon = this.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
});
```

### User Benefits
✅ Verify correct password before submitting  
✅ Prevent accidental account lockout  
✅ Improve login experience  

---

## 2. Application Deadline Countdown Timer

### What It Does
Displays real-time countdown to application deadline on applicant dashboard with visual urgency indicators.

### Where It's Available
- **Applicant Dashboard** - Top section
- **Application Detail Pages** (if deadline passed)

### How It Works

**Backend (Django View):**
```python
from applications.models import RegistrationSettings
from django.utils import timezone

settings = RegistrationSettings.objects.first()
deadline_info = {
    'deadline': settings.application_deadline.isoformat(),
    'is_open': timezone.now() <= settings.application_deadline
}
context['deadline_info'] = deadline_info
```

**Frontend Display:**
```html
<div id="countdown-timer" class="alert alert-warning">
    <h5>Application Deadline: <span id="countdown"></span></h5>
    <p>Days: <span id="days"></span> | Hours: <span id="hours"></span> | 
       Minutes: <span id="minutes"></span> | Seconds: <span id="seconds"></span></p>
</div>
```

**JavaScript Timer:**
```javascript
function startCountdown(deadline) {
    setInterval(function() {
        const now = new Date().getTime();
        const distance = new Date(deadline).getTime() - now;
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        document.getElementById('days').innerText = days;
        document.getElementById('hours').innerText = hours;
        document.getElementById('minutes').innerText = minutes;
        document.getElementById('seconds').innerText = seconds;
        
        // Change color based on urgency
        if (days < 1) {
            timer.classList.add('alert-danger'); // Red
        } else if (days < 3) {
            timer.classList.add('alert-danger'); // Orange/Red
        }
    }, 1000);
}
```

### Features
✅ Real-time update every second  
✅ Visual urgency indicators (color changes)  
✅ Displays days, hours, minutes, seconds  
✅ Works across all user time zones  
✅ Updates on page load  

---

## 3. Deadline Enforcement

### What It Prevents
After application deadline passes:
- ❌ New applications cannot be submitted
- ❌ Only applications can be viewed (no changes)
- ❌ Documents cannot be added/modified

### Where Checks Occur

**Step 1 (School/Program Selection):**
```python
settings = RegistrationSettings.objects.first()
if timezone.now() > settings.application_deadline and not app.submitted_date:
    messages.error(request, 'Application deadline has passed')
    return redirect('applications:dashboard')
```

**Step 2, 3, 4:**
- Similar checks before allowing data modification
- Only allows cancellation or viewing

**Application Submission:**
```python
if not deadline_info['is_open']:
    messages.error(request, 'Cannot submit: Application deadline passed')
    return redirect('applications:dashboard')
```

### For Admins
⚠️ Registration CAN continue after deadline  
⚠️ Only application submission is blocked  

---

## 4. Super Admin Profile Improvements

### What Changed
Super Admins no longer see location fields in their profile.

### Profile Visibility

**For Super Admins:**
```
- Account Status: Active ✅
- User Type: Super Admin
- Verification Status: System User
- Location: NOT REQUIRED FOR SUPER ADMINS
```

**For Regular Admins/Users:**
```
- County: [Displayed]
- Ward: [Displayed]
```

### Edit Profile Form

**Super Admin Edit:**
- Location fields hidden
- Info alert: "Location information is not required for Super Admins"
- Other fields editable

**Regular User Edit:**
- Location fields visible
- Required for location-based filtering

---

## 5. Enhanced Permission System

### New Helper Function: `get_admin_role_type()`

**Purpose:** Safely retrieve admin type without errors

**Code:**
```python
def get_admin_role_type(user):
    """Safely get admin role type"""
    if user.is_superuser:
        return 'Super_Admin'
    try:
        if hasattr(user, 'admin_role') and user.admin_role:
            return user.admin_role.role_type
    except:
        pass
    return 'Super_Admin'
```

**Usage:**
```python
admin_type = get_admin_role_type(request.user)
if admin_type == 'Ward_Admin':
    # Ward-specific logic
elif admin_type == 'CDF_Admin':
    # CDF-specific logic
elif admin_type == 'Super_Admin':
    # System-wide access
```

### Improved `is_admin()` Check

```python
def is_admin(user):
    """Check if user is admin"""
    # Super Admins
    if user.is_superuser:
        return True
    # Django staff without role (safe)
    if user.is_staff:
        try:
            if user.admin_role:
                return True
        except:
            pass
        return True  # Staff without role still admin
    return False
```

---

## 6. Application Multi-Step Form

### 4-Step Workflow

**Step 1: School Selection**
- Select institution type (University/TVET/College)
- Choose school
- Select program
- Confirm before proceeding

**Step 2: Personal Information**
- Date of birth
- Gender
- National ID (fraud prevention)
- Ward/Constituency selection
- Phone number

**Step 3: Document Upload**
- Student ID/Admission letter
- Birth certificate
- National ID
- Other supporting documents
- Real-time validation

**Step 4: Review**
- Summary of all information
- Confirmation checkbox
- Final submission button
- Cannot modify after submit

### Data Persistence
- Saved as draft after each step
- Resume later capability
- Auto-save on step completion

---

## 7. Application Tracking

### Applicant Can See
- Current application status
- Last update date/time
- Comments from admins
- Documents uploaded
- Application timeline

### Status Flow
```
Draft → Submitted → Under_Review → Approved → Amount_Awarded
                                     ↓
                                  Rejected
```

### Notifications
- Email on status change
- Notifications in-app
- Summary available on dashboard

---

## 8. Document Management

### Supported Formats
- PDF
- JPG/JPEG
- PNG
- DOC/DOCX

### Upload Validation
- File size limit: 5MB
- Type validation
- Virus scan ready (framework available)
- Privacy protection

### Features
- Download as PDF
- Export as CSV
- Batch download
- Archive functionality

---

## 9. Admin Dashboard Features

### Super Admin Dashboard
- **View All:** All applications system-wide
- **Statistics:** System-wide metrics
- **Recent Apps:** Latest 10 submissions
- **Pending Count:** Total pending review
- **Filters:** By status, school, program

### Ward Admin Dashboard
- **Ward Only:** Applications from assigned ward
- **Pending:** Awaiting doc verification
- **Statistics:** Ward-specific metrics
- **Actions:** Approve/reject buttons

### CDF Admin Dashboard
- **County View:** All approved applications
- **Award Form:** Enter bursary amounts
- **Statistics:** County-level reports
- **Export:** Generate reports

---

## 10. Notification System

### Triggers
- Application submitted
- Document uploaded
- Status changed
- Deadline reminder (24h before)
- Fraudulent activity detected

### Channels
- **Email:** Default
- **SMS:** Framework ready
- **In-App:** Dashboard notifications

### Templates
- System includes 10+ pre-built templates
- Customizable per event
- Variable support (applicant name, award amount, etc.)

---

## 11. Reporting Features

### Available Reports
- Application statistics by school
- Ward-wise distribution
- Award summaries
- Program popularity
- Fraud incidents

### Export Formats
- CSV
- PDF (with logo)
- JSON

### Auto-Generated
- Monthly summaries
- Quarterly reviews
- Annual reports

---

## 12. Fraud Prevention

### Detection Methods
- Duplicate National ID checks
- Duplicate application detection
- Unusual pattern recognition
- Admin verification flags
- Multiple account detection

### Block Actions
- Prevent duplicate registration
- Flag suspicious apps
- Log attempts in audit trail
- Alert admins automatically

---

## Feature Timeline

| Feature | Release | Status |
|---------|---------|--------|
| Core Application | v1.0 | ✅ Complete |
| Multi-level Approval | v1.0 | ✅ Complete |
| Document Upload | v1.0 | ✅ Complete |
| Notifications | v1.0 | ✅ Complete |
| Password Toggle | Feb 2026 | ✅ Complete |
| Countdown Timer | Feb 2026 | ✅ Complete |
| Deadline Enforcement | Feb 2026 | ✅ Complete |
| Super Admin Improvements | Feb 2026 | ✅ Complete |

---

**For implementation details, see [System Architecture](System-Architecture.md)**
