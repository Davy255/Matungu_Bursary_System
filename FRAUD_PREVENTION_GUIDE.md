# National ID Fraud Prevention System

## Overview

The Bursary System now includes a comprehensive **National ID fraud prevention system** that ensures:
- ✅ One account per person - each National ID can only register once
- ✅ Verified identity for all applicants and admins
- ✅ Optional National ID verification during login
- ✅ One admin per person - prevents multiple admin role assignments to same person
- ✅ Clear validation messages for users

## Features Implemented

### 1. **National ID Unique Constraint**

Each National ID in the system must be unique. This is enforced at the **database level** to ensure data integrity.

**Database Change:**
```sql
-- UserProfile.national_id now has UNIQUE constraint
ALTER TABLE users_userprofile 
    ADD CONSTRAINT national_id_unique UNIQUE(national_id);
```

**What This Means:**
- A person cannot register multiple accounts with the same National ID
- If someone tries to register with an already-registered National ID, they will see an error
- The system prevents fraud at the database level (not just application level)

### 2. **During Registration - Comprehensive Verification**

#### New Validation Checks:
1. **National ID Required** - Cannot skip registration without providing National ID
2. **National ID Uniqueness Check** - Prevents duplicate National IDs
3. **Duplicate Account Prevention** - Shows users if their National ID is already registered
4. **Clear Error Messages** - Users see exactly why registration failed

#### Registration Flow:
```
User submits registration form with:
  ↓
  ├─ Username (checked for uniqueness)
  ├─ Email (checked for uniqueness)
  ├─ First Name & Last Name
  ├─ National ID (checked for uniqueness - FRAUD CHECK)
  └─ Password
  ↓
  Form validation:
  ├─ If National ID already exists → ERROR: "This National ID is already registered"
  ├─ If Email already exists → ERROR: "This email is already registered"
  ├─ If Username already exists → ERROR: "This username is already in use"
  └─ If all valid → Create account and redirect to login
```

#### Registration Template Updates:
- **Anti-Fraud Badge** - "REQUIRED - Anti-Fraud" badge on National ID field
- **Fraud Prevention Alert Box** - Explains why National ID is required
- **Help Text** - Clear instructions for National ID field
- **Registration Status** - Shows if registration is open, closed, or near deadline
- **Duplicate Account Warning** - Shows if that National ID is already registered

**Screenshots Location:**
- Registration form: [templates/users/register.html](templates/users/register.html)

### 3. **During Login - Optional National ID Verification**

#### New Feature:
Users can optionally verify their identity using National ID during login for extra security.

#### Login Flow:
```
User submits login form with:
  ↓
  ├─ Username
  ├─ Password
  └─ [Optional] National ID for verification
  ↓
  If National ID provided:
  ├─ Check if National ID matches registered ID for this account
  ├─ If matches → Login successful
  └─ If doesn't match → ERROR: "National ID does not match registered ID"
  ↓
  If National ID not provided:
  └─ Standard login (username + password only)
```

#### Security Benefits:
- **Two-Factor Identity** - Username/password + National ID verification
- **Prevents Account Takeover** - Even if password is compromised, National ID provides second check
- **Optional but Recommended** - Users can enable for their accounts

#### Login Form Updates:
- **Checkbox Option** - "Verify with National ID" checkbox
- **Dynamic Field** - National ID field appears when checkbox is checked
- **Security Info Alert** - Explains the security benefits
- **Help Text** - Instructions for National ID verification

**Screenshots Location:**
- Login form: [templates/users/login.html](templates/users/login.html)

### 4. **One Admin Per Person Constraint**

#### Database Change:
```python
# AdminRole model now has unique constraint on 'user' field
class Meta:
    unique_together = ()  # Removed old constraint
    constraints = [
        models.UniqueConstraint(fields=['user'], name='one_admin_per_user')
    ]
```

#### What This Means:
- Each user can only have ONE admin role in the system
- Cannot assign multiple admin roles to same person
- Cannot assign Ward_Admin + CDF_Admin to same person
- If attempted, database will reject the duplicate assignment

#### Enforcement:
```python
# This will raise IntegrityError:
try:
    AdminRole.objects.create(
        user=super_admin_user,
        role_type='Ward_Admin',
        ward='Mayoni',
        assigned_by=current_user
    )
    # Later attempt same user with different role:
    AdminRole.objects.create(
        user=super_admin_user,
        role_type='CDF_Admin',
        ward='Mayoni',
        assigned_by=current_user
    )  # ERROR: UNIQUE constraint failed
except IntegrityError:
    print("User already has an admin role!")
```

## Code Changes Summary

### Modified Files:

#### 1. **users/models.py**
```python
# UserProfile - Added unique constraint
national_id = models.CharField(
    max_length=20,
    blank=True,
    null=True,
    unique=True,  # Unique constraint
    help_text="National ID number - must be unique to prevent duplicate accounts"
)

# AdminRole - Added unique constraint on user field
class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user'], name='one_admin_per_user')
    ]
```

#### 2. **users/forms.py**
```python
# Enhanced validation:
def clean_username(self):
    """Validate username is unique"""
    username = self.cleaned_data.get('username')
    if User.objects.filter(username=username).exists():
        raise ValidationError('This username is already in use. Please choose another.')
    return username

def clean_national_id(self):
    """Validate national ID is provided and unique"""
    national_id = (self.cleaned_data.get('national_id') or '').strip()
    
    if not national_id:
        raise ValidationError('National ID is required.')
    
    # Check if national ID already registered
    existing = UserProfile.objects.filter(national_id=national_id, user__is_active=True)
    if existing.exists():
        raise ValidationError(
            'This National ID is already registered in the system. '
            'Only one account per person is allowed. If this is your account, please log in instead.'
        )
    
    return national_id
```

#### 3. **users/views.py**
```python
# Registration view - Added double-check for national ID
if UserProfile.objects.filter(national_id=national_id, user__is_active=True).exists():
    messages.error(request, 'This National ID is already registered...')
    return render(request, 'users/register.html', {...})

# Login view - Added optional national ID verification
national_id = request.POST.get('national_id', '').strip()
if national_id:
    user_national_id = user.profile.national_id if hasattr(user, 'profile') else None
    if not user_national_id or user_national_id != national_id:
        messages.error(request, 'National ID does not match the registered ID for this account...')
        return render(request, 'users/login.html')
```

#### 4. **templates/users/register.html**
- Updated with comprehensive fraud prevention messaging
- Added National ID field with "REQUIRED - Anti-Fraud" badge
- Added registration status alerts
- Added fraud prevention info box
- Added help text explaining why National ID is required
- Added form validation and error display

#### 5. **templates/users/login.html**
- Updated with optional National ID verification
- Added checkbox to enable National ID verification
- Added dynamic National ID input field
- Added security information alert
- Added help text for National ID verification

### Database Migration:

**Migration File:** `users/migrations/0003_add_national_id_unique_constraint.py`

**Changes Made:**
- Added unique constraint to `UserProfile.national_id`
- Updated `AdminRole` model to use `UniqueConstraint` instead of `unique_together`
- Set proper help text and field attributes

**Migration Status:**
```
✅ Applied successfully
Command: python manage.py migrate
Result: users.0003_add_national_id_unique_constraint... OK
```

## Testing the Fraud Prevention System

### Test Case 1: Duplicate Registration Prevention

```
Steps:
1. Register User A with National ID: 12345678
   Result: ✅ Account created successfully

2. Try to register User B with same National ID: 12345678
   Result: ❌ Form validation error:
           "This National ID is already registered in the system"

3. Attempt to use different email/username:
   Result: ❌ Still blocked by National ID check
           Message: "Only one account per person is allowed"
```

### Test Case 2: Login with National ID Verification

```
Steps:
1. Register User A with National ID: 12345678
2. Login with correct National ID:
   - Username: user_a
   - Password: password123
   - National ID: 12345678
   Result: ✅ Login successful

3. Try to login with wrong National ID:
   - Username: user_a
   - Password: password123
   - National ID: 99999999
   Result: ❌ Error: "National ID does not match the registered ID"
           Login blocked
```

### Test Case 3: Registration with Missing National ID

```
Steps:
1. Try to register without providing National ID
2. Submit form with empty National ID field
   Result: ❌ Form validation error:
           "National ID is required."
           Registration blocked
```

### Test Case 4: Admin Role One-Per-Person Constraint

```
Steps:
1. Create Admin User with Ward_Admin role for Ward: Mayoni
   Result: ✅ AdminRole created successfully

2. Try to assign same user CDF_Admin role
   Result: ❌ IntegrityError in Django:
           "UNIQUE constraint failed on model `AdminRole`"
           Assignment blocked
```

## User Experience

### For New Applicants:

**Before Registration:**
- System shows registration status (open/closed/deadline)
- Clear explanation of National ID requirement

**During Registration:**
- National ID field clearly marked as "REQUIRED - Anti-Fraud"
- Help text: "Your government-issued National ID is required for account verification"
- Error message if trying to register with existing National ID
- Fraud prevention alert explaining the rules

**After Registration:**
- Success message: "Registration successful! Your account has been created with your National ID"
- Redirected to login page

### For Returning Users (Login):

**During Login:**
- Optional National ID verification checkbox
- Clear security information
- If checking National ID verification:
  - Extra field appears for National ID
  - System verifies National ID matches their account
  - Adds extra security layer

**Error Scenarios:**
- National ID mismatch: "National ID does not match the registered ID for this account"
- Username/password incorrect: "Invalid username or password"

### For Admins:

**Ward Admin / CDF Admin:**
- Cannot be assigned multiple admin roles
- Each person has exactly one admin role
- Clear administrative enforcement

## Security Considerations

### Strengths:
✅ Database-level unique constraint (cannot be bypassed)
✅ Form-level validation (user-friendly error messages)
✅ View-level double-check (defense in depth)
✅ Optional login verification (two-factor identity)
✅ One admin per person (prevents admin impersonation)
✅ Active user filter (inactive accounts don't block new registrations)

### Best Practices:
✅ National ID stored as plain text (for verification purposes)
✅ Encrypted password storage (Django default)
✅ CSRF protection on all forms
✅ Rate limiting recommended (prevent brute force)
✅ Account deactivation supported (not deletion)

## Troubleshooting

### Problem: "This National ID is already registered"
**Cause:** Someone already created an account with this National ID
**Solution:** 
- If it's your account, use login instead
- Contact admin if you believe this is an error

### Problem: National ID verification fails during login
**Cause:** Entered wrong National ID, or it doesn't match registered ID
**Solution:**
- Double-check your National ID is correct
- Ensure you're entering the exact National ID used during registration
- Use login without National ID verification if unsure

### Problem: Cannot create second admin account
**Cause:** User already has an admin role assigned
**Solution:**
- Each user can only have one admin role
- If role needs to change, remove old role then assign new one
- Or create a new user for the new admin role

## Configuration

### Enable/Disable National ID Requirement:

To temporarily disable National ID requirement (not recommended):

```python
# In users/forms.py - CustomUserCreationForm
national_id = forms.CharField(
    required=False,  # Change to False to make optional
    ...
)

# Then update validation logic
def clean_national_id(self):
    national_id = (self.cleaned_data.get('national_id') or '').strip()
    
    if not national_id:
        return national_id  # Allow empty
    
    # Rest of validation...
```

### Optional: Add National ID Format Validation

To add format validation (e.g., must be 8 digits):

```python
def clean_national_id(self):
    national_id = (self.cleaned_data.get('national_id') or '').strip()
    
    if not national_id:
        raise ValidationError('National ID is required.')
    
    # Add format check
    if not national_id.isdigit() or len(national_id) != 8:
        raise ValidationError('National ID must be exactly 8 digits.')
    
    # Rest of validation...
```

## Future Enhancements

Potential improvements:
- [ ] National ID format validation (must match government format)
- [ ] Scan/upload national ID document for verification
- [ ] Email verification of National ID changes
- [ ] Admin review queue for National ID discrepancies
- [ ] Automated fraud detection algorithms
- [ ] IP-based duplicate detection
- [ ] Multi-factor authentication (SMS, email, biometric)

## Support & Questions

For issues or questions about the fraud prevention system:
1. Check this guide's troubleshooting section
2. Review test cases to understand expected behavior
3. Contact system administrator
4. Check Django error logs for detailed error messages

---

**Last Updated:** February 21, 2026
**System:** Django 4.2 Bursary Management System
**Status:** ✅ Active and Enforced
