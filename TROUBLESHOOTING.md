# Troubleshooting Guide for HealthHub

## Common Issues & Solutions

### Installation Issues

#### 1. Python Version Mismatch

**Error:**
```
Error: Python 3.14 is needed but Python 3.10 is installed
```

**Solution:**
```bash
# Check Python version
python --version

# Install correct version from python.org
# Then create virtual environment with correct version
python3.10 -m venv venv
source venv/bin/activate
```

#### 2. Virtual Environment Not Activating

**Windows:**
```bash
# Run this instead of venv/Scripts/activate
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Check if activated:**
```bash
which python  # Should show path in venv
```

#### 3. pip Not Found

**Error:**
```
pip: command not found
```

**Solution:**
```bash
# Use Python module invocation
python -m pip install -r requirements.txt

# Or upgrade pip
python -m pip install --upgrade pip
```

#### 4. Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'django'
```

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
python -c "import django; print(django.get_version())"
```

### Database Issues

#### 1. Database Migration Errors

**Error:**
```
django.core.management.base.SystemCheckError: System check identified some issues
```

**Solution:**
```bash
# Check for existing migrations
python manage.py showmigrations

# Create missing migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# If stuck, reset (development only!)
python manage.py migrate --plan  # See what will happen first
```

#### 2. SQLite Database Locked

**Error:**
```
database is locked
```

**Solution:**
```bash
# Force close all connections
python manage.py shell
>>> from django.db import connection
>>> connection.close()

# Or restart Django shell/server

# Check for locks
lsof | grep db.sqlite3  # Mac/Linux

# Delete corrupted database (dev only)
rm db.sqlite3
python manage.py migrate
```

#### 3. PostgreSQL Connection Issues

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/healthhub

# Test connection
psql -U username -d healthhub -h localhost

# If password issues
sudo -u postgres psql
ALTER USER "healthhub_user" WITH PASSWORD 'new_password';
```

#### 4. Database Already Exists Error

**Error:**
```
database "health hub" already exists
```

**Solution:**
```bash
# List databases
psql -l

# Drop database (careful!)
psql
DROP DATABASE healthhub;
CREATE DATABASE healthhub;

# Or specify different name in .env
```

### Django Issues

#### 1. Secret Key Not Set

**Error:**
```
Traceback (most recent call last):
  ...
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.
```

**Solution:**
```bash
# Copy .env.example to .env
cp .env.example .env

# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add to .env
SECRET_KEY=your_generated_key_here
```

#### 2. Static Files Not Found

**Error:**
```
Static file not found: /static/css/style.css
```

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings.py STATIC_URL and STATIC_ROOT are set
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# In development, ensure DEBUG=True
DEBUG=True
```

#### 3. Media Files Not Accessible

**Error:**
```
404: Media file not found
```

**Solution:**
```bash
# Create media directory
mkdir -p media

# Check settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# In development, add to urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 4. CSRF Token Missing

**Error:**
```
Forbidden (403)
CSRF verification failed. Request aborted.
```

**Solution:**
```python
# In template, include CSRF token
{% csrf_token %}

# In AJAX requests
$(document).ready(function() {
    var csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

# Or use JavaScript utility from main.js
getCookie('csrftoken')
```

### Authentication Issues

#### 1. Login Not Working

**Error:**
```
Invalid username/password - even with correct credentials
```

**Solution:**
```bash
# Check user exists
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.filter(username='testuser').first()
>>> user.check_password('password123')  # Should return True

# Create new test user if needed
python manage.py createsuperuser
```

#### 2. Role-Based Access Not Working

**Error:**
```
Users not redirected to correct dashboard based on role
```

**Solution:**
```python
# Check user.role in settings
# In healthhub/views.py login view, verify redirects:

if user.role == 'patient':
    return redirect('patient_dashboard')
elif user.role == 'doctor':
    return redirect('doctor_dashboard')
elif user.role == 'hospital_admin':
    return redirect('hospital_dashboard')

# Verify role values in CustomUser model choices
```

#### 3. Session Expires Too Quickly

**Error:**
```
User logged out after short period
```

**Solution:**
```python
# In settings.py, adjust session timeout
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# For development, extend timeout
if DEBUG:
    SESSION_COOKIE_AGE = 604800  # 7 days
```

### API Issues

#### 1. API Returns 401 Unauthorized

**Error:**
```
{
    "detail": "Authentication credentials were not provided."
}
```

**Solution:**
```bash
# Ensure you're sending Authorization header
Authorization: Token your_token_here

# Get token first
curl -X POST http://localhost:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# In Python requests
import requests
login_response = requests.post(
    'http://localhost:8000/api-auth/login/',
    json={'username': 'user', 'password': 'pass'}
)
token = login_response.json()['key']

headers = {'Authorization': f'Token {token}'}
response = requests.get('http://localhost:8000/api/patients/', headers=headers)
```

#### 2. API Returns 403 Forbidden

**Error:**
```
{
    "detail": "You do not have permission to perform this action."
}
```

**Solution:**
```python
# Check permission_classes in viewset
class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # User must be logged in
    
    # Or use more granular permissions
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAuthenticated()]
```

#### 3. API Returns CORS Errors

**Error:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/' 
from origin 'http://localhost:3000' has been blocked
```

**Solution:**
```bash
# Install django-cors-headers
pip install django-cors-headers

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]

# Add middleware (before CommonMiddleware)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Or allow all (development only)
CORS_ALLOW_ALL_ORIGINS = True
```

#### 4. API Pagination Not Working

**Error:**
```
Returns all results instead of paginated
```

**Solution:**
```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Use in requests
GET /api/patients/?page=1
GET /api/patients/?page=2
```

### WebSocket Issues

#### 1. WebSocket Connection Failed

**Error:**
```
WebSocket connection failed
```

**Solution:**
```bash
# Ensure running with ASGI (not WSGI)
daphne -b 0.0.0.0 -p 8000 healthhub.asgi:application

# Not
python manage.py runserver  # Uses WSGI, no WebSocket

# Check CHANNEL_LAYERS in settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# For production, use Redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

#### 2. Messages Not Appearing in Chat

**Error:**
```
User sends message but it doesn't appear
```

**Solution:**
```python
# Check consumers.py is properly configured
# Verify WebSocket URL pattern in routing.py
websocket_urlpatterns = [
    path("ws/chat/<int:room_id>/", ChatConsumer.as_asgi()),
]

# Test WebSocket connection
from channels.testing import WebsocketCommunicator

async def test_chat():
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "ws/chat/1/")
    connected, subprotocol = await communicator.connect()
    assert connected
```

#### 3. Connection Drops Frequently

**Error:**
```
WebSocket disconnected unexpectedly
```

**Solution:**
```python
# Add reconnection logic in JavaScript
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

function connectWebSocket() {
    chatSocket = new WebSocket(wsProtocol + window.location.host + wsPath);
    
    chatSocket.onclose = function(e) {
        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            setTimeout(connectWebSocket, 3000);
            reconnectAttempts++;
        }
    };
}

# Increase timeout settings
CHANNEL_LAYER_CAPACITY = 1500
```

### Performance Issues

#### 1. Slow Database Queries

**Solution:**
```bash
# Enable Django Debug Toolbar
pip install django-debug-toolbar

# Add to INSTALLED_APPS
'debug_toolbar',

# Add middleware
'debug_toolbar.middleware.DebugToolbarMiddleware',

# Configure allowed hosts for toolbar
INTERNAL_IPS = ['127.0.0.1']

# Include in urls.py
from django.conf import settings
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls))
```

#### 2. Memory Usage High

**Solution:**
```python
# Use select_related() for ForeignKey
Patient.objects.select_related('user').all()

# Use prefetch_related() for ManyToMany
Doctor.objects.prefetch_related('hospitals').all()

# Use only() to fetch specific fields
Patient.objects.only('id', 'user_id', 'blood_group')

# Use values() for dictionaries instead of objects
Patient.objects.values('id', 'blood_group')
```

#### 3. API Endpoints Slow

**Solution:**
```python
# Add caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def patient_list(request):
    pass

# Use select_for_update() for read operations
Doctor.objects.select_for_update().filter(id=1)

# Optimize serializers
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'user_id', 'blood_group')  # Only needed fields
```

### Email Issues

#### 1. Emails Not Sending

**Error:**
```
No email sent
```

**Solution:**
```bash
# Check .env has correct credentials
MAILTRAP_API_TOKEN=your_token

# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])

# Check logs
# Mailtrap shows "Email Delivery" status

# If using development, use console backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### 2. Mailtrap Authentication Failed

**Error:**
```
SMTPAuthenticationError: SMTP AUTH extension not supported by server
```

**Solution:**
```bash
# Verify Mailtrap credentials in .env
MAILTRAP_HOST=smtp.mailtrap.io
MAILTRAP_PORT=587  # or 465 for TLS
MAILTRAP_USER=your_username
MAILTRAP_PASSWORD=your_password

# Use TLS
EMAIL_USE_TLS = True

# Test connection
telnet smtp.mailtrap.io 587
```

### Payment Issues

#### 1. SSLCommerz Gateway Not Responding

**Error:**
```
Payment gateway timeout
```

**Solution:**
```python
# Check .env has credentials
SSLCOMMERZ_STORE_ID=your_store_id
SSLCOMMERZ_STORE_PASSWORD=your_password

# Verify endpoint (sandbox vs production)
SSLCOMMERZ_PAYMENT_URL = 'https://sandbox.sslcommerz.com/'  # Dev
SSLCOMMERZ_PAYMENT_URL = 'https://securepay.sslcommerz.com/'  # Prod

# Test payment
python manage.py shell
>>> from payments.views import initiate_payment
>>> response = initiate_payment(appointment, 50.00)
```

#### 2. Webhook Not Received

**Error:**
```
Payment status not updated
```

**Solution:**
```python
# Add logging to payment webhook handler
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def payment_webhook(request):
    logger.info(f"Webhook received: {request.POST}")
    # Process webhook
    return JsonResponse({'status': 'success'})

# Configure SSLCommerz to call correct URL
# Settings > Webhook URL: http://yourdomain.com/payments/webhook/

# Check webhook in SSLCommerz dashboard
# Test webhook manually
curl -X POST http://localhost:8000/payments/webhook/ \
  -d "tran_id=1234&status=VALID"
```

## Debugging Tools

### Django Shell

```bash
python manage.py shell

# Check data
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.first()
print(user.__dict__)

# Modify data
user.email = 'newemail@example.com'
user.save()

# Run query
from patients.models import Patient
Patient.objects.filter(blood_group='O+').count()
```

### View SQL Queries

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:
    queryset = Patient.objects.all()
    print(f"Queries: {len(ctx)}")
    for query in ctx:
        print(query['sql'])
```

### Check Email Sending

```python
# Use console backend in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Emails will print to console instead of sending
```

### Inspect Request/Response

```python
# In view
print(f"Method: {request.method}")
print(f"User: {request.user}")
print(f"POST: {request.POST}")
print(f"GET: {request.GET}")
print(f"Headers: {request.META}")
```

## Getting More Help

1. **Check Logs**
   ```bash
   tail -f logs/django.log
   ```

2. **Enable Django Logging**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
           },
       },
       'root': {
           'handlers': ['console'],
           'level': 'DEBUG',
       },
   }
   ```

3. **Search Issues**
   - Search GitHub Issues
   - Check Django Documentation
   - Search StackOverflow

4. **Report Issues**
   - Include error message
   - Include Python/Django versions
   - Include steps to reproduce
   - Include relevant logs
