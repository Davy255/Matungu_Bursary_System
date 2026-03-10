# MySQL Database Setup Guide
## Bursary Management System

This guide will help you configure MySQL as the database backend for the Bursary Management System.

---

## 📋 Prerequisites

Before you begin, make sure you have:
- Python 3.9 or higher installed
- MySQL Server 8.0 or higher installed
- pip (Python package manager)

---

## 🛠️ Step 1: Install MySQL Server

### Windows:
1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Run the installer and select **"MySQL Server"**
3. During setup, set a **root password** (remember this!)
4. Complete the installation

### Verify Installation:
```powershell
mysql --version
```

You should see something like: `mysql Ver 8.0.xx`

---

## 🔧 Step 2: Install MySQL Client for Python

The Python MySQL connector (`mysqlclient`) is required for Django to communicate with MySQL.

### Install mysqlclient:

**Windows (PowerShell):**
```powershell
# Activate your virtual environment first
.\.venv\Scripts\Activate.ps1

# Install mysqlclient
pip install mysqlclient
```

**If you encounter errors on Windows**, you may need to install Visual C++ Build Tools:
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install with "Desktop development with C++" workload
3. Then retry: `pip install mysqlclient`

**Alternative (if mysqlclient fails):**
```powershell
pip install pymysql
```

Then add this to your `__init__.py` in the project root:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## 🗄️ Step 3: Create MySQL Database

### Option A: Using MySQL Workbench (GUI - Recommended for Beginners)

1. Open **MySQL Workbench**
2. Connect to your local MySQL server (localhost)
3. Click **"Create New Schema"** icon
4. Name it: `bursary_db`
5. Click **"Apply"**

### Option B: Using Command Line

```powershell
# Login to MySQL as root
mysql -u root -p
# Enter your root password when prompted
```

Then in the MySQL shell:
```sql
-- Create database
CREATE DATABASE bursary_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify database was created
SHOW DATABASES;

-- Exit MySQL shell
EXIT;
```

---

## ⚙️ Step 4: Configure Django Settings

### 1. Copy the .env.example file to .env:
```powershell
Copy-Item .env.example .env
```

### 2. Edit the .env file with your MySQL credentials:

**Open `.env` in a text editor and update:**

```env
# MySQL Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=bursary_db
DB_USER=root
DB_PASSWORD=YourMySQLPasswordHere  # ← Change this to your actual MySQL root password
DB_HOST=localhost
DB_PORT=3306
```

**Important Security Notes:**
- ⚠️ Never commit the `.env` file to Git
- ⚠️ Use a strong password for MySQL
- ⚠️ The `.env` file is already in `.gitignore`

---

## 📦 Step 5: Update requirements.txt

Add `mysqlclient` to your `requirements.txt`:

```txt
Django==6.0.2
djangorestframework==3.14.0
django-cors-headers==4.2.0
python-decouple==3.8
Pillow==10.0.0
mysqlclient==2.2.0  # ← MySQL connector
gunicorn==21.2.0
python-dotenv==1.0.0
celery==5.3.1
redis==5.0.0
```

---

## 🚀 Step 6: Run Django Migrations

Once your database is configured:

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run migrations to create tables
python manage.py makemigrations
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

---

## ✅ Step 7: Verify Database Connection

### Test in Django Shell:
```powershell
python manage.py shell
```

Then in the Python shell:
```python
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT DATABASE();")
print(cursor.fetchone())  # Should print: ('bursary_db',)
exit()
```

---

## 🔍 Verify Tables Were Created

### Using MySQL Workbench:
1. Open MySQL Workbench
2. Connect to localhost
3. Select `bursary_db` database
4. Click **Tables** → you should see Django tables

### Using Command Line:
```powershell
mysql -u root -p bursary_db
```

Then:
```sql
-- Show all tables
SHOW TABLES;

-- Expected output (example):
-- +----------------------------+
-- | Tables_in_bursary_db       |
-- +----------------------------+
-- | auth_user                  |
-- | users_userprofile          |
-- | applications_application   |
-- | schools_school             |
-- | ...                        |
-- +----------------------------+

EXIT;
```

---

## 🎯 Step 8: Create Django Superuser

Create an admin account to access the Django admin panel:

```powershell
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin`
- Email: your email
- Password: (create a strong password)

---

## 🌐 Step 9: Run Development Server

```powershell
python manage.py runserver
```

Visit:
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

Login with the superuser credentials you created.

---

## 🔧 Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"

**Solution:**
- Check your password in `.env` file matches your MySQL root password
- Try resetting MySQL root password:
  ```powershell
  mysql -u root -p
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
  FLUSH PRIVILEGES;
  EXIT;
  ```

### Error: "Unknown database 'bursary_db'"

**Solution:**
- Make sure you created the database (Step 3)
- Check database name spelling in `.env` file

### Error: "Can't connect to MySQL server on 'localhost'"

**Solution:**
- Make sure MySQL service is running:
  ```powershell
  # Check MySQL service status (Windows)
  Get-Service MySQL*
  
  # Start MySQL service if stopped
  Start-Service MySQL80  # Or your MySQL service name
  ```

### Error: "mysqlclient install fails on Windows"

**Solution 1:** Install Visual C++ Build Tools
- Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install and retry

**Solution 2:** Use PyMySQL instead:
```powershell
pip install pymysql
```

Then create `__init__.py` in your project root:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## 📊 Database Management Tips

### Backup Database:
```powershell
mysqldump -u root -p bursary_db > backup.sql
```

### Restore Database:
```powershell
mysql -u root -p bursary_db < backup.sql
```

### Reset Database (Development Only):
```powershell
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS bursary_db; CREATE DATABASE bursary_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations again
python manage.py migrate
```

---

## 🔐 Security Best Practices

### For Development:
1. ✅ Use strong MySQL root password
2. ✅ Never commit `.env` file to Git
3. ✅ Keep `DEBUG=True` only in development

### For Production:
1. ✅ Create a dedicated MySQL user (not root):
   ```sql
   CREATE USER 'bursary_user'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT ALL PRIVILEGES ON bursary_db.* TO 'bursary_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
2. ✅ Set `DEBUG=False` in production
3. ✅ Use environment variables for sensitive data
4. ✅ Enable MySQL SSL connections

---

## 📚 Useful MySQL Commands

```sql
-- Show all databases
SHOW DATABASES;

-- Use a specific database
USE bursary_db;

-- Show all tables
SHOW TABLES;

-- Describe table structure
DESCRIBE users_userprofile;

-- Show table creation SQL
SHOW CREATE TABLE applications_application;

-- Count records in a table
SELECT COUNT(*) FROM users_userprofile;

-- View recent applications
SELECT * FROM applications_application ORDER BY created_at DESC LIMIT 10;
```

---

## ✅ Verification Checklist

Before proceeding with development, make sure:

- [ ] MySQL Server is installed and running
- [ ] Database `bursary_db` is created
- [ ] `mysqlclient` is installed in your virtual environment
- [ ] `.env` file is configured with correct MySQL credentials
- [ ] `python manage.py migrate` runs successfully
- [ ] Django admin page loads at http://localhost:8000/admin
- [ ] You can login with your superuser account

---

## 🎉 Success!

Your Bursary Management System is now configured to use MySQL!

**Next Steps:**
1. Start implementing the Django models (users, applications, schools)
2. Create views and templates
3. Test the application workflow
4. Refer to `COMPLETE_DEVELOPER_GUIDE.md` for full implementation details

---

**Need Help?**
- MySQL Documentation: https://dev.mysql.com/doc/
- Django MySQL Notes: https://docs.djangoproject.com/en/5.0/ref/databases/#mysql-notes
- mysqlclient on GitHub: https://github.com/PyMySQL/mysqlclient

---

**Last Updated:** March 2026  
**Status:** Ready for Development with MySQL
