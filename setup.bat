# Setup script for HealthHub on Windows

@echo off
echo ======================================
echo HealthHub Setup Script for Windows
echo ======================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Copy .env file
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env with your configuration
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo Creating admin user...
echo Please enter admin credentials:
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create media directories
echo Creating media directories...
if not exist media mkdir media
if not exist media\profile_images mkdir media\profile_images
if not exist media\doctor_certificates mkdir media\doctor_certificates
if not exist media\hospital_logos mkdir media\hospital_logos
if not exist media\lab_reports mkdir media\lab_reports
if not exist media\chat_files mkdir media\chat_files

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To run the development server:
echo   python manage.py runserver
echo.
echo To run with WebSocket support:
echo   daphne -b 0.0.0.0 -p 8000 healthhub.asgi:application
echo.
echo Access the application at:
echo   http://localhost:8000
echo.
echo Admin panel at:
echo   http://localhost:8000/admin
echo.
pause
