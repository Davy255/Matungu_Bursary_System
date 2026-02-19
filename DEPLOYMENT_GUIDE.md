# Deployment Guide - Bursary Management System

This guide covers deploying the Bursary Management System to production environments.

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code reviewed and merged
- [ ] Database backed up
- [ ] Environment variables configured
- [ ] SSL certificate obtained
- [ ] Domain name configured
- [ ] Email service configured
- [ ] SMS service configured

## Deployment Options

### Option 1: Ubuntu Server with Gunicorn & Nginx

#### Prerequisites
- Ubuntu 20.04 LTS
- Python 3.8+
- PostgreSQL or MySQL
- Nginx
- Supervisor

#### Installation

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3.8 python3-pip python3-venv
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y nginx supervisor
sudo apt-get install -y git
```

#### Clone Repository

```bash
cd /var/www
sudo git clone https://github.com/yourusername/bursary-system.git
cd bursary-system
```

#### Create Django User

```bash
sudo useradd -m -s /bin/bash django
sudo chown -R django:django /var/www/bursary-system
```

#### Set Up Virtual Environment

```bash
sudo -u django python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure Environment

```bash
cp .env.example .env
sudo nano .env
# Edit with production settings
```

#### Run Migrations

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

#### Configure Gunicorn

Create file: `/var/www/bursary-system/gunicorn_config.py`

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5
```

#### Create Systemd Service

```bash
sudo nano /etc/systemd/system/bursary.service
```

```ini
[Unit]
Description=Bursary Management System
After=network.target

[Service]
User=django
WorkingDirectory=/var/www/bursary-system
Environment="PATH=/var/www/bursary-system/venv/bin"
ExecStart=/var/www/bursary-system/venv/bin/gunicorn \
    --config /var/www/bursary-system/gunicorn_config.py \
    --env DJANGO_SETTINGS_MODULE=bursary_system.settings \
    bursary_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start bursary
sudo systemctl enable bursary
```

#### Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/bursary
```

```nginx
upstream bursary {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    client_max_body_size 5M;
    
    location /static/ {
        alias /var/www/bursary-system/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/bursary-system/media/;
    }
    
    location / {
        proxy_pass http://bursary;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/bursary /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Set Up SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Git initialized
- Heroku account

#### Configuration Files

Create `Procfile`:
```
web: gunicorn bursary_system.wsgi
release: python manage.py migrate
```

Create `runtime.txt`:
```
python-3.9.18
```

#### Deploy

```bash
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create mailgun:starter

git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 3: Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bursary_system.wsgi:application"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: bursary_system
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn bursary_system.wsgi:application --bind 0.0.0.0:8000"
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      DEBUG: "False"
      DB_ENGINE: django.db.backends.mysql
      DB_NAME: bursary_system
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_HOST: db
      DB_PORT: "3306"
    depends_on:
      - db

volumes:
  db_data:
```

Deploy:
```bash
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
```

## Post-Deployment Steps

### 1. Verify Installation

```bash
# Check if application is running
curl https://yourdomain.com

# Check logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 2. Create Initial Admin User

```bash
python manage.py createsuperuser
```

### 3. Load Initial Data

```bash
python manage.py populate_schools
```

### 4. Configure Email

1. Set up email service (Gmail, SendGrid, etc.)
2. Configure SMTP settings in `.env`

### 5. Configure SMS

1. Set up Twilio account
2. Add credentials to `.env`
3. Create SMS templates in admin panel

### 6. Set Up Backups

```bash
# Daily database backup
0 2 * * * mysqldump -u root -p'password' bursary_system > /backups/db-$(date +\%Y\%m\%d).sql

# Add to crontab
crontab -e
```

### 7. Monitor Application

```bash
# Check application status
systemctl status bursary

# View error logs
journalctl -u bursary -f

# Monitor resource usage
top
```

## Performance Optimization

### 1. Enable Caching

Add to `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2. Database Optimization

- Add indexes to frequently queried fields
- Use select_related() and prefetch_related()
- Archive old records

### 3. Static Files

- Use CDN for static assets
- Enable gzip compression
- Minify CSS and JavaScript

### 4. Media Files

- Use object storage (S3, Google Cloud Storage)
- Enable file compression
- Implement cleanup of old files

## Security Hardening

### 1. Firewall

```bash
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw status
```

### 2. Fail2Ban

```bash
sudo apt-get install fail2ban
sudo systemctl start fail2ban
```

### 3. Keep Systems Updated

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get autoremove
```

### 4. Regular Backups

- Daily database backups
- Weekly full system backups
- Store backups in secure location
- Test backup restoration regularly

## Monitoring & Alerts

### 1. Application Monitoring

Set up monitoring for:
- Application uptime
- Response times
- Error rates
- Database performance

### 2. Send Alerts

Configure alerts for:
- High CPU usage
- High memory usage
- Database connection errors
- Application crashes

### 3. Log Aggregation

- Use ELK Stack or similar
- Centralize logs
- Set up alerts based on logs

## Rollback Procedure

In case of issues:

```bash
# Rollback to previous version
git log --oneline
git revert <commit-hash>
git push heroku main

# Or restore from backup
mysql -u root -p bursary_system < backup_file.sql
```

## Troubleshooting

### Issue: Application won't start

```bash
systemctl status bursary
journalctl -u bursary
```

### Issue: Database connection errors

```bash
mysql -u root -p bursary_system
SHOW TABLES;
```

### Issue: Static files not loading

```bash
python manage.py collectstatic --clear --noinput
```

### Issue: Email not sending

- Check email configuration
- Verify credentials
- Check logs for errors

## Maintenance Schedule

- **Daily**: Check application logs, verify backups
- **Weekly**: Review error rates, update packages
- **Monthly**: Security updates, performance analysis
- **Quarterly**: Security audit, capacity planning

---

For production support, contact your hosting provider or DevOps team.
