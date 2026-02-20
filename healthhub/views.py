# Core views for auth and homepage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from patients.forms import CustomUserCreationForm

User = get_user_model()


def home(request):
    """Home page"""
    return render(request, 'home/index.html')


@require_http_methods(["GET", "POST"])
def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create patient profile if registering as patient
            if user.role == 'patient':
                from patients.models import Patient
                Patient.objects.get_or_create(user=user)
            
            # Log in the user after registration
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'patient':
                return redirect('patient_dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            elif user.role == 'hospital_admin':
                return redirect('hospital_admin_dashboard')
            elif user.role == 'lab_worker':
                return redirect('labs:worker_dashboard')
            elif user.role == 'pharmacist':
                return redirect('pharmacy:pharmacist_dashboard')
            
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'form_error': 'Invalid credentials'})
    
    return render(request, 'auth/login.html')


@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    return redirect('home')
