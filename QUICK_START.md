# Quick Start Guide for HealthHub

Get the HealthHub platform running in 5 minutes!

## Prerequisites

- Python 3.10+ ([Download Here](https://www.python.org/downloads/))
- Git ([Download Here](https://git-scm.com/))
- A modern web browser

## 1️⃣ Installation (2 minutes)

### Windows

```batch
# Clone the repository
git clone https://github.com/R-dev-07/healthhub.git
cd healthhub

# Run setup script
setup.bat

# Wait for completion...
```

### Mac/Linux

```bash
# Clone the repository
git clone https://github.com/R-dev-07/healthhub.git
cd healthhub

# Make script executable and run
chmod +x setup.sh
./setup.sh

# Wait for completion...
```

### Manual Setup (If scripts don't work)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Create superuser (follow prompts - use admin/admin123)
```

## 2️⃣ Start the Server (30 seconds)

```bash
# Make sure virtual environment is activated
python manage.py runserver

# Server running at http://localhost:8000
```

**For WebSocket (Real-time Chat):**

```bash
# Install Daphne
pip install daphne

# Run with ASGI
daphne -b 0.0.0.0 -p 8000 healthhub.asgi:application
```

## 3️⃣ Create Test Account

Visit: [http://localhost:8000/register](http://localhost:8000/register)

Create account as:
- **Patient** - Book appointments, buy medicines, order lab tests
- **Doctor** - Manage appointments, create prescriptions
- **Hospital Admin** - Manage hospital operations
- **Pharmacist** - Manage medicine inventory
- **Lab Worker** - Process lab tests

## 4️⃣ Explore the App

### For Patients
1. Go to [Dashboard](http://localhost:8000/patients/dashboard/)
2. Search for doctors or hospitals
3. Book an appointment
4. View prescriptions
5. Chat with your doctor

### For Doctors
1. Complete your profile
2. Register with hospitals
3. View pending appointments
4. Accept/reject appointments
5. Create prescriptions

### For Hospital Admins
1. Go to [Dashboard](http://localhost:8000/hospitals/dashboard/)
2. Add departments
3. Manage staff
4. View hospital statistics

## 5️⃣ Access Admin Panel

Visit: [http://localhost:8000/admin](http://localhost:8000/admin)

**Login with:**
- Username: `admin`
- Password: `admin123_change_me`

## API Testing

### Get API Token

```bash
curl -X POST http://localhost:8000/api-auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"R-dev-07","password":"your_password"}'
```

### Test API Endpoints

```bash
# List patients
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/patients/

# List doctors
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/doctors/

# List appointments
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/appointments/
```

## Environment Configuration

Edit `.env` file to customize:

```ini
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - uses SQLite by default)
# DATABASE_URL=postgresql://user:password@localhost:5432/healthhub

# Email (Mailtrap)
MAILTRAP_API_TOKEN=your-mailtrap-token

# Payment Gateway (SSLCommerz)
SSLCOMMERZ_STORE_ID=your-store-id
SSLCOMMERZ_STORE_PASSWORD=your-password

# Redis (optional - for caching/WebSocket layer)
REDIS_URL=redis://localhost:6379/0
```

## Project Structure Overview

```
healthhub/
├── manage.py                  # Django management
├── **/models.py              # Database models
├── **/views.py               # Endpoints & APIs
├── **/forms.py               # HTML forms
├── **/serializers.py         # API serializers
├── templates/                # HTML templates
├── static/                   # CSS, JavaScript
└── media/                    # User uploads
```

## Common Tasks

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test patients

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Create Database Backup

```bash
# SQLite
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL
pg_dump -U username healthhub > backup.sql
```

### Add New Data

```bash
# Use Django admin
http://localhost:8000/admin

# Or use Django shell
python manage.py shell
>>> from patients.models import Patient
>>> Patient.objects.create(...)
```

### Collect Static Files (Production)

```bash
python manage.py collectstatic --noinput
```

## Troubleshooting

### Server Won't Start?

```bash
# Check port is available
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Mac/Linux

# Use different port
python manage.py runserver 8001
```

### Module Not Found?

```bash
# Verify virtual environment is activated
python -m pip list | grep django

# Reinstall
pip install -r requirements.txt
```

### Database Error?

```bash
# Reset database (development only!)
python manage.py migrate --plan
python manage.py migrate

# Or
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading?

```bash
# Collect static files
python manage.py collectstatic --noinput

# Ensure DEBUG=True in .env for development
DEBUG=True
```

## Next Steps

1. **Read Full Documentation**: [README.md](README.md)
2. **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
5. **Testing**: [TESTING.md](TESTING.md)
6. **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Features You Can Explore

✅ **Patient Features**
- Search hospitals and doctors
- Book appointments
- Order lab tests
- Purchase medicines
- Real-time chat with doctors
- Download prescriptions (PDF)
- Leave doctor reviews

✅ **Doctor Features**
- Complete profile setup
- Register with hospitals
- Manage appointments
- Create prescriptions
- View patient history
- Real-time patient chat

✅ **Hospital Management**
- Department management
- Doctor registration
- Service offerings
- Department with bed tracking

✅ **Lab Services**
- Test catalog
- Online ordering
- Report generation
- PDF downloads

✅ **Pharmacy**
- Medicine catalog
- Shopping cart
- Order tracking
- Prescription-based medicine

✅ **Payment System**
- SSLCommerz integration
- Multiple payment methods
- Refund requests
- Transaction history

✅ **Real-time Chat**
- Doctor-patient messaging
- Message history
- File sharing
- Typing indicators

## Command Reference

```bash
# Virtual environment
python -m venv venv           # Create
source venv/bin/activate      # Activate (Mac/Linux)
venv\Scripts\activate         # Activate (Windows)
deactivate                     # Deactivate

# Django
python manage.py migrate          # Run migrations
python manage.py makemigrations   # Create migrations
python manage.py runserver        # Run development server
python manage.py test             # Run tests
python manage.py createsuperuser  # Create admin
python manage.py shell            # Python shell
python manage.py collectstatic    # Collect static files

# Database
python manage.py dbshell          # Database shell
python manage.py flush            # Clear all data
python manage.py loaddata         # Load fixtures

# Maintenance
python manage.py check            # Check for issues
python manage.py showmigrations   # Show migration status
```

## Getting Help

🆘 **Having Issues?**

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search in [GitHub Issues](https://github.com/R-dev-07/healthhub/issues)
3. Check [Django Documentation](https://docs.djangoproject.com/)
4. Ask in [GitHub Discussions](https://github.com/R-dev-07/healthhub/discussions)

## Support & Community

- 📖 Full Documentation: [README.md](README.md)
- 🐛 Report Bugs: [GitHub Issues](https://github.com/R-dev-07/healthhub/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/R-dev-07/healthhub/discussions)
- 📧 Email: support@healthhub.example.com
- 💬 Chat: [Discord Community](https://discord.gg/your-invite)

---

**Happy coding! 🚀**

If you found HealthHub helpful, please ⭐ star the repository!
