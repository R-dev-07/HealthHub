# HealthHub - Multi-Hospital Health Management Platform

A comprehensive Django-based health management platform enabling efficient tracking, monitoring, and sharing of patient health records across multiple hospitals.

## Project Overview

HealthHub is a sophisticated software system that connects multiple hospitals, doctors, patients, and pharmacies in a unified ecosystem. It facilitates appointment booking, prescription management, laboratory testing, medicine purchasing, and real-time doctor-patient communication.

## Features

### Patient Features
- Search multiple hospitals and their departments
- Search and filter doctors by specialization
- Book appointments with doctors
- Pay for appointments with online payment integration
- Chat in real-time with appointed doctors
- View and download prescriptions (PDF)
- Select and pay for laboratory tests
- View and download laboratory reports
- Leave reviews and ratings for doctors
- Search and purchase medicines from pharmacy
- Track medication orders and delivery

### Doctor Features
- Complete doctor profile setup and management
- Register with multiple hospitals
- Accept/reject patient appointment requests
- Search and view patient profiles
- Create and manage prescriptions
- Chat with patients
- View patient reports and test results
- Manage availability and consultation fees

### Hospital Admin Features
- Hospital dashboard and management
- Accept/reject doctor registrations
- Create and manage hospital departments
- Manage hospital services
- Add and manage lab workers
- Add and manage pharmacists
- View hospital analytics

### Pharmacist Features
- Pharmacist dashboard
- Add, edit, and manage medicines
- Set medicine prices and stock levels
- Search medicines
- View and manage customer orders
- Track medicine inventory

### Lab Worker Features
- Lab dashboard with pending tests
- Upload and manage test reports
- Generate PDF reports
- Track test samples

## Tech Stack

### Backend
- **Framework**: Django 4.2 (Python Web Framework)
- **API**: Django REST Framework
- **Real-time**: Django Channels with WebSocket
- **Database**: SQLite (Development), PostgreSQL (Production)

### Frontend
- Bootstrap 5 for UI
- JavaScript & AJAX for interactions
- HTML/CSS/JS templates

### External Integrations
- **Payment Gateway**: SSLCommerz (Debit Card, Credit Card, Mobile Banking)
- **Email Service**: Mailtrap (Development), SMTP (Production)
- **PDF Generation**: xhtml2pdf and Django PDF Library
- **Chat**: Django Channels with WebSocket

### Additional Libraries
- Pillow - Image handling
- Django Widget Tweaks - Form rendering
- Django Debug Toolbar - Development debugging
- django-environ - Environment variable management

## Project Structure

```
healthhub/                  # Main project configuration
├── settings.py            # Project settings
├── urls.py               # URL routing
├── asgi.py               # ASGI configuration (Channels)
├── wsgi.py               # WSGI configuration

patients/                  # Patient app
├── models.py             # CustomUser, Patient, PatientReview
├── views.py              # Patient views
├── urls.py               # Patient URLs

doctors/                   # Doctor app
├── models.py             # Doctor, DoctorHospitalRegistration, Prescription
├── views.py              # Doctor views
├── urls.py               # Doctor URLs

hospitals/                 # Hospital app
├── models.py             # Hospital, Department, HospitalService
├── views.py              # Hospital views
├── urls.py               # Hospital URLs

labs/                      # Laboratory app
├── models.py             # LabTest, LabReport, LabTestOrder
├── views.py              # Lab views
├── urls.py               # Lab URLs

pharmacy/                  # Pharmacy app
├── models.py             # Medicine, MedicineOrder, Pharmacist
├── views.py              # Pharmacy views
├── urls.py               # Pharmacy URLs

appointments/              # Appointment app
├── models.py             # Appointment
├── views.py              # Appointment views
├── urls.py               # Appointment URLs

payments/                  # Payment app
├── models.py             # Payment, PaymentGatewayConfig, RefundRequest
├── views.py              # Payment views
├── urls.py               # Payment URLs

chat/                      # Chat app
├── models.py             # ChatRoom, Message
├── views.py              # Chat views
├── consumers.py          # WebSocket consumers
├── routing.py            # WebSocket routing
├── urls.py               # Chat URLs

templates/                 # HTML templates
static/                    # Static files (CSS, JS, images)
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Step 1: Clone & Setup Environment
```bash
git clone <repository-url>
cd healthhub
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 4: Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Step 5: Create Sample Data (Optional)
```bash
python manage.py loaddata sample_data
```

### Step 6: Run Development Server
```bash
# For HTTP only (no WebSocket)
python manage.py runserver

# For HTTP + WebSocket (requires Daphne)
daphne -b 0.0.0.0 -p 8000 healthhub.asgi:application
```

## Database Models Summary

### Users & Authentication
- **CustomUser**: Extended Django User model with roles (patient, doctor, hospital_admin, lab_worker, pharmacist)
- **Patient**: Patient profile with medical information
- **Doctor**: Doctor profile with qualifications and specialization

### Healthcare Management
- **Hospital**: Hospital information and details
- **Department**: Hospital departments
- **Appointment**: Doctor-patient appointments
- **Prescription**: Doctor prescriptions for patients
- **LabTest**: Available laboratory tests
- **LabReport**: Patient lab test results
- **Medicine**: Available medicines in pharmacy

### Business Operations
- **MedicineOrder**: Customer medicine purchases
- **LabTestOrder**: Customer lab test bookings
- **Payment**: Transaction records
- **ChatRoom**: Doctor-Patient conversations
- **Message**: Individual chat messages

## API Endpoints

### RESTful APIs
All APIs require authentication. Base URL: `/api/v1/`

- **/patients/api/users/** - User management
- **/patients/api/patients/** - Patient profiles
- **/doctors/api/doctors/** - Doctor listings
- **/hospitals/api/hospitals/** - Hospital listings
- **/labs/api/tests/** - Available lab tests
- **/pharmacy/api/medicines/** - Medicine listings
- **/appointments/api/appointments/** - Appointment management
- **/payments/api/payments/** - Payment history
- **/chat/api/chat-rooms/** - Chat rooms

## WebSocket Endpoints

Real-time chat via WebSocket:
```
ws://localhost:8000/ws/chat/{chat_room_id}/
```

## Configuration Guide

### Email Configuration (Mailtrap)
1. Sign up at [Mailtrap](https://mailtrap.io)
2. Get SMTP credentials
3. Update .env file with EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

### Payment Gateway (SSLCommerz)
1. Register at [SSLCommerz](https://www.sslcommerz.com)
2. Get Store ID and Password
3. Update .env file with SSLCOMMERZ credentials

### Redis Cache (Optional)
```bash
# Install Redis
# Update settings.py for caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## Deployment

### Production Checklist
1. Set `DEBUG=False` in .env
2. Generate a strong SECRET_KEY
3. Configure PostgreSQL database
4. Set up proper ALLOWED_HOSTS
5. Configure SSL/HTTPS
6. Set up email backend (SendGrid, AWS SES, etc.)
7. Enable CSRF, security headers
8. Use Gunicorn + Nginx
9. Set up Celery for background tasks
10. Configure logging

### Deployment Example (Gunicorn)
```bash
gunicorn healthhub.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test patients

# Run with verbosity
python manage.py test --verbosity=2
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

This project is part of a B.Sc. in Computer Science and Engineering (CSE) Software Engineering Project.

## Support & Documentation

For detailed API documentation, visit `/api/docs/` (after installing drf-spectacular)

## Future Enhancements

- [ ] Prescription API integration with local pharmacies
- [ ] Telemedicine video consultation
- [ ] Mobile app (iOS/Android)
- [ ] AI-based symptom checker
- [ ] Health insurance integration
- [ ] Appointment reminders (SMS/Email)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Appointment waiting list system
- [ ] Prescription auto-refill
