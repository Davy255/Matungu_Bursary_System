# 🔐 Fraud Prevention Quick Reference

## What's Protected?
- ✅ Cannot register multiple accounts with same National ID
- ✅ One National ID = One Account (enforced at database level)
- ✅ Optional login verification using National ID
- ✅ Each person can only have one admin role

## 🚨 Key Rules
1. **National ID is REQUIRED** - Cannot register without it
2. **National ID must be UNIQUE** - Each ID registers only once
3. **Registration shows status** - Open/closed/deadline alerts
4. **Login is optional with National ID** - Can verify for extra security
5. **Admins are one-per-person** - Cannot have multiple admin roles

## 📋 Validation Checklist

### For Users Registering:
- [ ] Provide unique username
- [ ] Provide unique email
- [ ] Provide valid National ID
- [ ] Ensure National ID not already registered
- [ ] Create strong password
- [ ] Confirm password

### For Users Logging In:
- [ ] Enter correct username
- [ ] Enter correct password
- [ ] Optionally verify with National ID
- [ ] If using National ID verification, must match registered ID

### For Admins:
- [ ] Each user can have only one admin role
- [ ] Cannot assign multiple roles to same person
- [ ] Role assignment enforced at database level

## 🔍 Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "This National ID is already registered" | Someone already has this ID registered | Use login instead if this is your account |
| "This username is already in use" | Username already registered | Choose a different username |
| "This email is already registered" | Email already in system | Use different email or login |
| "National ID is required" | Tried to register without National ID | Provide your National ID |
| "National ID does not match" | Entered wrong ID during login verification | Verify you entered correct National ID |

## 📊 Database Constraints

```
UserProfile.national_id
├─ Type: CharField (max 20 chars)
├─ Unique: YES ✅ (cannot have duplicates)
├─ Required: YES ✅ (cannot be blank during registration)
└─ Hidden: NO (shown to user during registration & verification)

AdminRole.user
├─ Type: OneToOneField
├─ Constraint: Unique ✅ (one admin per person)
└─ Enforcement: Database level (cannot bypass)
```

## 🛠️ Configuration

### Where is National ID?
- **In Registration:** Required field with "REQUIRED - Anti-Fraud" badge
- **In Login:** Optional verification checkbox + field

### How to Access?
- **Registration:** `/register/`
- **Login:** `/login/`

### Help Text Shown:
```
Registration:
"Your government-issued National ID is required for account 
verification. This prevents fraud and ensures only you can 
access your account. Each National ID can only be used once."

Login:
"For added security, you can verify your identity using your 
National ID. This helps prevent unauthorized access to your account."
```

## 🚀 Testing

### Quick Test 1 - Duplicate Prevention
1. Register: user1@test.com, ID: 12345678
2. Try Register: user2@test2.com, ID: 12345678
3. Expected: ❌ Error - "National ID already registered"

### Quick Test 2 - Login Verification
1. Login with username + password ✅ Works
2. Login with username + password + correct National ID ✅ Works
3. Login with username + password + wrong National ID ❌ Fails

### Quick Test 3 - Admin Constraint
1. Assign user as Ward_Admin ✅ Works
2. Try to assign same user as CDF_Admin ❌ Error

## 📞 Support

### For Registration Issues
- If National ID is rejected: Compare with previously used ID
- If get "already registered" error: Use login if it's your account
- If National ID field missing: Refresh page or contact admin

### For Login Issues
- If National ID verification fails: Double-check entered ID matches
- If not sure of National ID: Uncheck verification (optional feature)
- If cannot login: Check username/password first

### For Admin Issues
- If cannot create second admin: First admin must be removed
- If role assignment fails: Check user doesn't already have admin role

## 📈 Statistics Tracked

For each registration:
- ✅ Username (must be unique)
- ✅ Email (must be unique)
- ✅ National ID (must be unique)
- ✅ Account creation timestamp
- ✅ Account verification status

For each login:
- ✅ Successful/failed login attempts
- ✅ National ID verification (if enabled)
- ✅ Verification success/failure
- ✅ User type & role

## 🎓 Best Practices

✅ **DO:**
- Store your National ID safely
- Use National ID verification for extra security
- Report duplicate account attempts to admin
- Keep your password secure

❌ **DON'T:**
- Share your National ID with others
- Use same passwords across accounts
- Try to register multiple accounts (will fail and be flagged)
- Give admin access to unauthorized users

## 📝 System Files

**Key Files Modified:**
- `users/models.py` - National ID constraint added
- `users/forms.py` - Validation enhanced
- `users/views.py` - Verification logic added
- `templates/users/register.html` - UI redesigned
- `templates/users/login.html` - Verification UI added
- `users/migrations/0003_add_national_id_unique_constraint.py` - Schema updated

**Documentation Files:**
- `FRAUD_PREVENTION_GUIDE.md` - Comprehensive guide
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `QUICK_REFERENCE.md` - This file

## ✅ Verification Status

```
[✓] Database constraints applied
[✓] Form validation working
[✓] Registration protection active
[✓] Login verification available
[✓] Admin role enforcement active
[✓] No system errors
[✓] All migrations applied
[✓] UI properly configured
```

## 🔐 Security Levels

**Level 1: Registration** (Mandatory)
- National ID required
- Unique constraint enforced
- Prevents duplicate accounts

**Level 2: Login** (Optional)
- Optional National ID verification
- Extra security layer
- Recommended for sensitive accounts

**Level 3: Admin** (Enforced)
- One admin per person
- Database level protection
- Cannot assign multiple roles

---

**For complete information:** See `FRAUD_PREVENTION_GUIDE.md`  
**System Status:** ✅ **ACTIVE AND PROTECTING**

*Last Updated: February 21, 2026*
