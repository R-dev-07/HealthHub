# Comprehensive Deployment Guide for HealthHub

## Pre-Deployment Checklist

- [ ] All tests pass
- [ ] No debug statements in code
- [ ] Environment variables configured
- [ ] Database backups created
- [ ] Static files collected
- [ ] Security settings verified
- [ ] SSL certificates installed
- [ ] Email service configured

## Deployment Steps

### 1. Server Setup (Ubuntu/Debian)

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade

# Install Python and dependencies
sudo apt-get install python3 python3-pip python3-venv
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install redis-server
sudo apt-get install nginx
```

### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/R-dev-07/healthhub.git healthhub
cd healthhub

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE healthhub;
CREATE USER healthhub WITH PASSWORD 'strong-password';
ALTER ROLE healthhub SET client_encoding TO 'utf8';
ALTER ROLE healthhub SET default_transaction_isolation TO 'read committed';
ALTER ROLE healthhub SET default_transaction_deferrable TO ON;
ALTER ROLE healthhub SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE healthhub TO healthhub;
\q

# Configure .env file
cp .env.example .env
# Edit .env with production settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Create cache table
python manage.py createcachetable
```

### 3. Gunicorn Setup

```bash
# Create systemd service file
sudo nano /etc/systemd/system/healthhub.service

# Add this content:
[Unit]
Description=HealthHub Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/username/healthhub
ExecStart=/home/username/healthhub/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind unix:/run/gunicorn.sock \
    healthhub.wsgi:application

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable healthhub
sudo systemctl start healthhub
```

### 4. Nginx Configuration

```bash
# Create nginx config
sudo nano /etc/nginx/sites-available/healthhub

# Add this content:
upstream healthhub {
    server unix:/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    client_max_body_size 10M;

    location /static/ {
        alias /home/username/healthhub/staticfiles/;
    }

    location /media/ {
        alias /home/username/healthhub/media/;
    }

    location / {
        proxy_pass http://healthhub;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/healthhub /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Update Nginx config for HTTPS
sudo nano /etc/nginx/sites-available/healthhub
# (Update to use SSL certs)

# Auto-renewal
sudo systemctl enable certbot.timer
```

### 6. Celery Setup (for background tasks)

```bash
# Create Celery service
sudo nano /etc/systemd/system/healthhub-celery.service

# Add content for Celery worker and beat scheduler

sudo systemctl enable healthhub-celery
sudo systemctl start healthhub-celery
```

### 7. Monitoring & Logging

```bash
# View application logs
sudo journalctl -u healthhub -f

# Monitor Redis
redis-cli monitor

# Monitor database
sudo -u postgres psql healthhub
\l  # List databases
\dt # List tables
```

## Maintenance

### Regular Backups

```bash
# Database backup
pg_dump healthhub > /backups/healthhub-$(date +%Y%m%d).sql

# Media files backup
tar -czf /backups/media-$(date +%Y%m%d).tar.gz media/

# Automated backup script (add to cron)
# 0 2 * * * /home/username/healthhub/backup.sh
```

### Updates

```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart healthhub
sudo systemctl restart nginx
```

## Performance Optimization

### Database Optimization

```sql
CREATE INDEX idx_patient_user ON patients_patient(user_id);
CREATE INDEX idx_appointment_date ON appointments_appointment(appointment_date);
CREATE INDEX idx_payment_status ON payments_payment(status);
```

### Caching

```python
# In settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}
```

### CDN Configuration

Use CloudFlare or similar CDN for:
- Static files (CSS, JS, images)
- Media files (PDFs, images)
- API responses

## Security Hardening

1. **Django Settings**
   - Set `DEBUG = False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Enable security middleware
   - Set `SECURE_HSTS_SECONDS`

2. **Database**
   - Use strong passwords
   - Restrict database access
   - Enable SSL for database connections
   - Regular backups

3. **Server**
   - Enable firewall (UFW)
   - SSH key authentication
   - Fail2ban for brute-force protection
   - Regular security updates

4. **Application**
   - Keep dependencies updated
   - Regular security audits
   - Input validation
   - SQL injection protection (Django ORM handles this)
   - XSS protection (Django templates handle this)
   - CSRF protection enabled

## Troubleshooting

### Application Won't Start
```bash
sudo journalctl -u healthhub -n 50  # Check last 50 lines of logs
python manage.py check  # Check for configuration issues
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database Connection Error
```bash
sudo systemctl restart postgresql
python manage.py dbshell  # Test connection
```

### Memory Issues
```bash
free -h  # Check memory usage
sudo systemctl restart healthhub  # Restart application
```

## Monitoring Tools

- **Sentry**: Error tracking
- **New Relic**: Performance monitoring
- **Prometheus**: Metrics collection
- **ELK Stack**: Log aggregation
- **Grafana**: Dashboard visualization

## References

- Django Deployment Guide: https://docs.djangoproject.com/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/
- PostgreSQL: https://www.postgresql.org/
- Redis: https://redis.io/
- Let's Encrypt: https://letsencrypt.org/
