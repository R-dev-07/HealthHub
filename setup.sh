#!/bin/bash
# Setup script for HealthHub

echo "======================================"
echo "HealthHub Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# venv\Scripts\activate  # For Windows

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env with your configuration"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo "Creating admin user..."
echo "Please enter admin credentials:"
python manage.py createsuperuser

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create media directories
echo "Creating media directories..."
mkdir -p media/{profile_images,doctor_certificates,hospital_logos,lab_reports,chat_files}

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "To run the development server:"
echo "  python manage.py runserver"
echo ""
echo "To run with WebSocket support:"
echo "  daphne -b 0.0.0.0 -p 8000 healthhub.asgi:application"
echo ""
echo "Access the application at:"
echo "  http://localhost:8000"
echo ""
echo "Admin panel at:"
echo "  http://localhost:8000/admin"
echo ""
