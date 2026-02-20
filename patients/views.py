from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Patient, PatientReview, CustomUser
from .serializers import PatientSerializer, PatientReviewSerializer, CustomUserSerializer
from .forms import PatientProfileForm, PatientReviewForm


# API Views
class CustomUserViewSet(viewsets.ModelViewSet):
    """API ViewSet for Custom Users"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def current_user(self, request):
        """Get current logged-in user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PatientViewSet(viewsets.ModelViewSet):
    """API ViewSet for Patients"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)


class PatientReviewViewSet(viewsets.ModelViewSet):
    """API ViewSet for Patient Reviews"""
    queryset = PatientReview.objects.all()
    serializer_class = PatientReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PatientReview.objects.filter(patient__user=self.request.user)


# Function-based Views
@login_required
def patient_dashboard(request):
    """Patient dashboard view"""
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        patient = None
    
    context = {
        'patient': patient,
    }
    return render(request, 'patients/dashboard.html', context)


@login_required
def patient_profile(request):
    """Patient profile view"""
    patient = get_object_or_404(Patient, user=request.user)
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_profile')
    else:
        form = PatientProfileForm(instance=patient)
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'patients/profile.html', context)


@login_required
def patient_prescriptions(request):
    """View patient prescriptions"""
    patient = get_object_or_404(Patient, user=request.user)
    prescriptions = patient.prescriptions.all().order_by('-created_at')
    
    context = {
        'prescriptions': prescriptions,
    }
    return render(request, 'patients/prescriptions.html', context)


@login_required
def patient_reports(request):
    """View patient reports"""
    patient = get_object_or_404(Patient, user=request.user)
    reports = patient.lab_reports.all().order_by('-created_at')
    
    context = {
        'reports': reports,
    }
    return render(request, 'patients/reports.html', context)


@login_required
def search_hospitals(request):
    """Search for hospitals"""
    from hospitals.models import Hospital
    query = request.GET.get('q', '')
    hospitals = Hospital.objects.all()
    
    if query:
        hospitals = hospitals.filter(
            name__icontains=query
        ) | Hospital.objects.filter(address__icontains=query)
    
    context = {
        'hospitals': hospitals,
        'query': query,
    }
    return render(request, 'patients/search_hospitals.html', context)


@login_required
def search_doctors(request):
    """Search for doctors"""
    from doctors.models import Doctor
    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization', '')
    
    doctors = Doctor.objects.filter(is_verified=True)
    
    if query:
        doctors = doctors.filter(
            user__first_name__icontains=query
        ) | doctors.objects.filter(
            user__last_name__icontains=query
        )
    
    if specialization:
        doctors = doctors.filter(specialization=specialization)
    
    context = {
        'doctors': doctors,
        'query': query,
        'specialization': specialization,
    }
    return render(request, 'patients/search_doctors.html', context)


@login_required
def patient_appointments(request):
    """View patient appointments"""
    from appointments.models import Appointment
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'patients/appointments.html', context)


@login_required
def write_review(request, doctor_id):
    """Write a review for a doctor"""
    from doctors.models import Doctor
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = get_object_or_404(Patient, user=request.user)
    
    try:
        review = PatientReview.objects.get(patient=patient, doctor=doctor)
    except PatientReview.DoesNotExist:
        review = None
    
    if request.method == 'POST':
        form = PatientReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.patient = patient
            new_review.doctor = doctor
            new_review.save()
            return redirect('patient_dashboard')
    else:
        form = PatientReviewForm(instance=review)
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'patients/write_review.html', context)
