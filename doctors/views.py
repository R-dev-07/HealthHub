from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, DoctorHospitalRegistration, Prescription
from .serializers import DoctorSerializer, PrescriptionSerializer, DoctorHospitalRegistrationSerializer
from .forms import DoctorProfileForm, PrescriptionForm, DoctorHospitalRegistrationForm
from hospitals.models import Hospital


# API Views
class DoctorViewSet(viewsets.ModelViewSet):
    """API ViewSet for Doctors"""
    queryset = Doctor.objects.filter(is_verified=True)
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current doctor's profile"""
        try:
            doctor = request.user.doctor_profile
            serializer = self.get_serializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor profile not found'}, status=404)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a doctor"""
        doctor = self.get_object()
        reviews = doctor.reviews.all()
        from patients.serializers import PatientReviewSerializer
        serializer = PatientReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """API ViewSet for Prescriptions"""
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'doctor_profile'):
            return Prescription.objects.filter(doctor=user.doctor_profile)
        elif hasattr(user, 'patient_profile'):
            return Prescription.objects.filter(patient=user.patient_profile)
        return Prescription.objects.none()


# Function-based Views
@login_required
def doctor_dashboard(request):
    """Doctor dashboard"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return render(request, 'doctors/setup_profile.html')
    
    pending_appointments = doctor.appointments.filter(status='pending').count()
    total_patients = doctor.appointments.values('patient').distinct().count()
    pending_registrations = DoctorHospitalRegistration.objects.filter(
        doctor=doctor, status='pending'
    ).count()
    
    context = {
        'doctor': doctor,
        'pending_appointments': pending_appointments,
        'total_patients': total_patients,
        'pending_registrations': pending_registrations,
    }
    return render(request, 'doctors/dashboard.html', context)


@login_required
def doctor_profile_setup(request):
    """Setup or update doctor profile"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        doctor = None
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            new_doctor = form.save(commit=False)
            new_doctor.user = request.user
            new_doctor.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm(instance=doctor)
    
    context = {'form': form}
    return render(request, 'doctors/profile_setup.html', context)


@login_required
def doctor_hospitals(request):
    """List doctor's hospital registrations"""
    doctor = get_object_or_404(Doctor, user=request.user)
    registrations = DoctorHospitalRegistration.objects.filter(doctor=doctor)
    
    context = {
        'registrations': registrations,
        'doctor': doctor,
    }
    return render(request, 'doctors/hospitals.html', context)


@login_required
def register_hospital(request, hospital_id):
    """Register doctor with a hospital"""
    doctor = get_object_or_404(Doctor, user=request.user)
    hospital = get_object_or_404(Hospital, id=hospital_id)
    
    registration, created = DoctorHospitalRegistration.objects.get_or_create(
        doctor=doctor,
        hospital=hospital
    )
    
    if created:
        # Send email notification to hospital admin
        pass
    
    return redirect('doctor_hospitals')


@login_required
def doctor_patients(request):
    """List doctor's patients"""
    from appointments.models import Appointment
    doctor = get_object_or_404(Doctor, user=request.user)
    patients = doctor.appointments.filter(
        status__in=['approved', 'completed']
    ).values('patient').distinct()
    
    context = {
        'patients': patients,
        'doctor': doctor,
    }
    return render(request, 'doctors/patients.html', context)


@login_required
def doctor_appointments(request):
    """List doctor's appointments"""
    from appointments.models import Appointment
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'doctor': doctor,
        'status_filter': status_filter,
    }
    return render(request, 'doctors/appointments.html', context)


@login_required
def create_prescription(request, appointment_id):
    """Create prescription for a patient"""
    from appointments.models import Appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if appointment.doctor != doctor:
        return redirect('doctor_dashboard')
    
    try:
        prescription = Prescription.objects.get(appointment=appointment)
    except Prescription.DoesNotExist:
        prescription = None
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            new_prescription = form.save(commit=False)
            new_prescription.doctor = doctor
            new_prescription.patient = appointment.patient
            new_prescription.appointment = appointment
            new_prescription.save()
            return redirect('doctor_appointments')
    else:
        form = PrescriptionForm(instance=prescription)
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'doctors/create_prescription.html', context)


@login_required
def view_prescription(request, prescription_id):
    """View prescription"""
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if prescription.doctor != doctor and prescription.patient.user != request.user:
        return redirect('home')
    
    context = {'prescription': prescription}
    return render(request, 'doctors/view_prescription.html', context)
