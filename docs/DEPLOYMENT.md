# Deployment Guide

This guide covers deploying the Ecovest platform to various environments.

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 13+ (for production)
- Redis (for caching and background tasks)
- Git
- Domain name (for production)

## 🚀 Production Deployment

### Option 1: DigitalOcean App Platform

1. **Prepare your repository**
   ```bash
   # Ensure requirements.txt is up to date
   pip freeze > requirements.txt
   
   # Create runtime.txt (optional)
   echo "python-3.11.8" > runtime.txt
   ```

2. **Create app.yaml**
   ```yaml
   name: ecovest
   services:
   - name: web
     source_dir: /
     github:
       repo: YOUR_USERNAME/Ecovest
       branch: main
     run_command: gunicorn ecovest.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DEBUG
       value: "False"
     - key: ALLOWED_HOSTS
       value: "your-domain.com"
     - key: SECRET_KEY
       value: "your-secret-key"
     - key: DATABASE_URL
       value: "${db.DATABASE_URL}"
   
   databases:
   - name: db
     engine: PG
     version: "13"
     size: basic-xs
   ```

3. **Deploy**
   - Connect your GitHub repository
   - Configure environment variables
   - Deploy via DigitalOcean dashboard

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # Install Heroku CLI (varies by OS)
   # Create Procfile
   echo "web: gunicorn ecovest.wsgi:application" > Procfile
   ```

2. **Create and configure app**
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   heroku addons:create heroku-redis:hobby-dev
   
   # Set environment variables
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set SECRET_KEY=your-secret-key
   ```

3. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### Option 3: AWS EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.micro or larger
   - Configure security groups (HTTP, HTTPS, SSH)

2. **Setup server**
   ```bash
   # Connect via SSH
   ssh -i your-key.pem ubuntu@your-server-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3.11 python3.11-pip python3.11-venv
   sudo apt install postgresql postgresql-contrib
   sudo apt install nginx redis-server
   ```

3. **Deploy application**
   ```bash
   # Clone repository
   git clone https://github.com/YOUR_USERNAME/Ecovest.git
   cd Ecovest
   
   # Create virtual environment
   python3.11 -m venv venv
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   
   # Setup database
   sudo -u postgres createdb ecovest
   sudo -u postgres createuser --interactive
   
   # Configure environment
   cp .env.example .env
   # Edit .env with production settings
   
   # Run migrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Configure Nginx**
   ```nginx
   # /etc/nginx/sites-available/ecovest
   server {
       listen 80;
       server_name your-domain.com;
       
       location /static/ {
           alias /path/to/Ecovest/static/;
       }
       
       location /media/ {
           alias /path/to/Ecovest/media/;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

   ```bash
   # Enable site
   sudo ln -s /etc/nginx/sites-available/ecovest /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. **Setup Gunicorn service**
   ```ini
   # /etc/systemd/system/ecovest.service
   [Unit]
   Description=Ecovest Django App
   After=network.target
   
   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/Ecovest
   Environment="PATH=/home/ubuntu/Ecovest/venv/bin"
   ExecStart=/home/ubuntu/Ecovest/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 ecovest.wsgi:application
   
   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start ecovest
   sudo systemctl enable ecovest
   ```

## 🔧 Environment Configuration

### Production Settings

Create a production settings file:
```python
# ecovest/settings/production.py
from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/ecovest/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Environment Variables

Essential environment variables for production:

```bash
# Django
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Cache
CACHE_URL=redis://localhost:6379/1

# File Storage (AWS S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## 🔒 SSL/HTTPS Setup

### Using Certbot (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Verify auto-renewal
sudo certbot renew --dry-run
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Sentry for Error Tracking**
   ```bash
   pip install sentry-sdk[django]
   ```
   
   ```python
   # settings.py
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
   )
   ```

2. **Application Performance Monitoring**
   ```bash
   # Install New Relic
   pip install newrelic
   newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
   ```

### Log Management

```python
# settings/production.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/ecovest/django.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console'],
    },
}
```

## 🚦 Health Checks

Create health check endpoints:

```python
# core/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

## 📦 Database Migration

### Production Migration Strategy

```bash
# 1. Backup database
pg_dump ecovest > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Test migrations on staging
python manage.py migrate --dry-run

# 3. Apply migrations
python manage.py migrate

# 4. Verify application works
curl -f http://your-domain.com/health/
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.2
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /home/ubuntu/Ecovest
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          python manage.py migrate
          python manage.py collectstatic --noinput
          sudo systemctl restart ecovest
```

## 🆘 Troubleshooting

### Common Issues

1. **Static files not loading**
   ```bash
   python manage.py collectstatic --noinput
   # Check STATIC_ROOT and STATIC_URL settings
   ```

2. **Database connection errors**
   ```bash
   # Check DATABASE_URL format
   # Verify PostgreSQL is running
   sudo systemctl status postgresql
   ```

3. **Gunicorn not starting**
   ```bash
   # Check service logs
   sudo journalctl -u ecovest -f
   
   # Test gunicorn manually
   cd /path/to/Ecovest
   source venv/bin/activate
   gunicorn ecovest.wsgi:application
   ```

4. **SSL certificate issues**
   ```bash
   # Check certificate status
   sudo certbot certificates
   
   # Renew certificate
   sudo certbot renew
   ```

### Performance Optimization

1. **Enable caching**
   ```python
   # settings.py
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

2. **Database optimization**
   ```python
   # Use database connection pooling
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'OPTIONS': {
               'MAX_CONNS': 20,
               'MIN_CONNS': 5,
           }
       }
   }
   ```

3. **Static file optimization**
   ```bash
   # Install whitenoise for static file serving
   pip install whitenoise
   ```

For more detailed deployment guidance, see the [Django deployment documentation](https://docs.djangoproject.com/en/5.2/howto/deployment/).
