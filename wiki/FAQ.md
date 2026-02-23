# Frequently Asked Questions (FAQ)

## Installation & Setup

### Q: How do I install the system?
**A:** Follow the [Installation Guide](Installation-Guide.md). Quick steps:
```bash
git clone <repo>
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Q: What Python version is required?
**A:** Python 3.10 or higher. Check with `python --version`

### Q: How do I troubleshoot database errors?
**A:** Try:
```bash
python manage.py migrate zero
python manage.py migrate
```
See [Troubleshooting](Troubleshooting.md) for more solutions.

---

## User Management

### Q: How do I create a Super Admin?
**A:** Run:
```bash
python manage.py createsuperuser
# Enter username, email, password
```

### Q: How do I assign Ward Admin role?
**A:** 
1. Login as Super Admin
2. Go to Admin Panel → Manage Admins
3. Click "Assign New Admin Role"
4. Select user and assign ward
5. Click assign

### Q: Can I assign multiple roles to one user?
**A:** No, one user can only have one admin role or be applicant.

### Q: How do I change user password?
**A:** 
- User can go to Profile → Change Password
- Admin can go to /admin/auth/user/ and reset

---

## Applications

### Q: What is the application deadline?
**A:** Set by CDF Admin in Settings. Check dashboard countdown timer.

### Q: Can I submit application after deadline?
**A:** No, system blocks submission. Registration still open. See [Feature Guide](Feature-Guide.md#3-deadline-enforcement).

### Q: Can I edit my application after submission?
**A:** No, but you can add documents or communicate with admins.

### Q: What documents are required?
**A:** 
- Student ID/Admission letter
- Birth certificate
- National ID copy
- Plus any school-specific requirements

### Q: How long does approval take?
**A:** Typically 2-3 weeks:
- 1 week: Ward admin review
- 1-2 weeks: CDF admin amount award

### Q: How do I track my application?
**A:** Login and go to Dashboard → Track Application. See status, comments, timeline.

### Q: What if my application is rejected?
**A:** You'll receive email with reason. You can reapply next cycle.

---

## Admins & Approvals

### Q: What's the difference between Ward Admin and CDF Admin?
**A:** 
- **Ward Admin:** Reviews documents, approves/rejects
- **CDF Admin:** Approves amounts after ward approval

See [User Roles](User-Roles.md) for details.

### Q: How do I approve an application?
**A:** 
1. Go to Applications for Review
2. Click application row
3. Review documents
4. Enter comments
5. Click Approve or Reject

### Q: Can I see applications from other wards?
**A:** Ward Admins only see their ward. Super Admin sees all. CDF Admin sees county.

### Q: How do I award bursary amounts?
**A:** 
1. Go to CDF Admin → Approved Applications
2. Click "Award Amount"
3. Enter amount
4. Add comments (optional)
5. Submit

### Q: Can I undo an approval?
**A:** No, but Super Admin can manually modify via database.

---

## Technical Questions

### Q: Is the system secure?
**A:** Yes. Features include:
- CSRF protection
- SQL injection prevention
- XSS protection
- Password hashing
- National ID fraud detection
See [Security Guide](Security-Guide.md)

### Q: Can I use PostgreSQL?
**A:** Yes. Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Q: How do I backup the database?
**A:** 
```bash
# SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

### Q: How do I deploy to production?
**A:** See [Deployment Guide](Deployment-Guide.md)

### Q: Can I customize templates?
**A:** Yes. Edit templates in `templates/` folder. See [Development Setup](Development-Setup.md)

### Q: How do I add new user fields?
**A:** 
1. Edit `UserProfile` model
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update forms and templates

---

## Bugs & Errors

### Q: I see "RelatedObjectDoesNotExist: User has no admin_role"
**A:** Fixed in Feb 2026 update. Update code via git pull.

### Q: Application won't submit - "Deadline passed"
**A:** Check system deadline settings. Only applies after deadline.

### Q: Static files not loading
**A:** Run:
```bash
python manage.py collectstatic --clear --noinput
```

### Q: Can't login - "Too many failed attempts"
**A:** Wait 30 minutes or contact admin to reset.

### Q: Email not sending
**A:** Check `.env` EMAIL settings. In development, use console backend.

---

## Permissions & Access

### Q: Why can't I access admin panel?
**A:** You need admin role. Ask Super Admin to assign.

### Q: Can applicants see other applications?
**A:** No, only their own.

### Q: Can ward admins see applicants from other wards?
**A:** No, only their ward.

### Q: Why is "Location" hidden from my profile?
**A:** If you're Super Admin, location not required. Regular users see it.

---

## Features

### Q: How does password visibility toggle work?
**A:** Click eye icon on login/register to show/hide password. See [Feature Guide](Feature-Guide.md#1-password-visibility-toggle).

### Q: What does the countdown timer show?
**A:** Real-time countdown to application deadline. Turns red when less than 1 day remaining.

### Q: Can I export applications to CSV?
**A:** Yes. CDF Admin can export from "Approved Applications" page.

### Q: Does the system send notifications?
**A:** Yes, via email on status changes. SMS framework available.

---

## Performance

### Q: Why is the system slow?
**A:** Try:
1. Run on same network
2. Check database size (backup old data)
3. Disable debug mode in production
4. Increase server resources

### Q: How many concurrent users can it handle?
**A:** 
- Development: 1-5 users
- Production: 50+ with proper setup (Gunicorn + Nginx)

---

## Data

### Q: How long is data kept?
**A:** All data kept indefinitely unless manually deleted. Backups recommended.

### Q: Can I delete applications?
**A:** Only draft applications before submission. Super Admin can delete via /admin.

### Q: Can I export all data?
**A:** Yes, use management command:
```bash
python manage.py dumpdata > data_backup.json
```

### Q: Is there an audit trail?
**A:** Yes, all approvals logged in ApplicationApproval model.

---

## Getting Help

### Where do I report bugs?
**A:** GitHub Issues: https://github.com/your-username/Bursary_system/issues

### Who do I contact for support?
**A:** 
- Technical: IT Support
- Admin questions: Super Admin
- Development: See GitHub repo

### Is there documentation?
**A:** Yes! This wiki covers most topics. Start with [Home](Home.md)

---

## Glossary

| Term | Definition |
|------|-----------|
| **CDF** | County Development Fund |
| **Ward** | Administrative division (like constituency) |
| **Applicant** | Student applying for bursary |
| **Admin** | Staff member who reviews/approves applications |
| **Status** | Current state of application (Draft, Submitted, etc.) |
| **Deadline** | Last date to submit applications |

---

**Still have questions?** 

Check other wiki pages:
- [Installation Guide](Installation-Guide.md)
- [User Guide](User-Guide.md)
- [Admin Guide](Admin-Guide.md)
- [Troubleshooting](Troubleshooting.md)

Or open an issue on GitHub!
