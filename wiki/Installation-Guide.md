# Installation Guide

## Prerequisites

- **Python 3.10+**
- **pip** package manager
- **Git**
- **PostgreSQL** (for production) or SQLite (default for development)

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Bursary_system.git
cd Bursary_system
```

## Step 2: Create Virtual Environment

### On Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Environment Configuration

Create `.env` file in project root:

```bash
# Copy example
cp .env.example .env

# Edit .env with your settings
```

**Example `.env` content:**
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Step 5: Database Setup

### Initialize Database
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Load Initial Data
```bash
# Populate schools and programs
python manage.py populate_universities
python manage.py populate_tvets
python manage.py populate_colleges
python manage.py populate_schools

# Populate wards
python manage.py populate_wards

# Populate notification templates
python manage.py populate_notification_templates
```

## Step 6: Collect Static Files (Optional)

```bash
python manage.py collectstatic --noinput
```

## Step 7: Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Or use the provided bash script:

### Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1; python manage.py runserver 0.0.0.0:8000
```

### macOS/Linux
```bash
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

## Step 8: Access the Application

- **Application:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **API:** http://localhost:8000/api

## Verify Installation

```bash
# Run system checks
python manage.py check

# Run tests (if available)
python manage.py test
```

---

## Production Setup

### 1. Install Additional Dependencies
```bash
pip install gunicorn whitenoise psycopg2-binary
```

### 2. Configure Environment
```
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=generate-a-secure-random-key
```

### 3. Collect Static Files
```bash
python manage.py collectstatic
```

### 4. Run with Gunicorn
```bash
gunicorn bursary_system.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 5. Setup Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/bursary`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/project/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/bursary /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Troubleshooting

### Issue: Module not found errors
**Solution:** Ensure virtual environment is activated and all packages installed
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Database migration errors
**Solution:** Reset migrations (development only)
```bash
python manage.py migrate zero
python manage.py migrate
```

### Issue: Static files not loading
**Solution:** Collect static files
```bash
python manage.py collectstatic --clear --noinput
```

### Issue: Port 8000 already in use
**Solution:** Use different port
```bash
python manage.py runserver 8001
```

---

## Next Steps

- Read [Getting Started Guide](User-Guide.md) for end-users
- Read [Development Setup](Development-Setup.md) for developers
- Read [Deployment Guide](Deployment-Guide.md) for production
