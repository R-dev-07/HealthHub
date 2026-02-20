from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer
from .forms import AppointmentForm, AppointmentStatusForm, AppointmentRejectForm
from doctors.models import Doctor
from patients.models import Patient
from hospitals.models import Hospital


# API Views
class AppointmentViewSet(viewsets.ModelViewSet):
    """API ViewSet for Appointments"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return Appointment.objects.filter(patient=user.patient_profile)
        elif hasattr(user, 'doctor_profile'):
            return Appointment.objects.filter(doctor=user.doctor_profile)
        return Appointment.objects.none()


# Function-based Views
@login_required
def book_appointment(request, doctor_id):
    """Book an appointment with a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id, is_verified=True)
    patient = get_object_or_404(Patient, user=request.user)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.hospital = doctor.hospital_registrations.first().hospital if doctor.hospital_registrations.exists() else None
            appointment.save()
            
            # Send notification email
            return redirect('appointments:appointment_detail', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'appointments/book.html', context)


@login_required
def appointment_detail(request, appointment_id):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has access
    if hasattr(request.user, 'patient_profile'):
        if appointment.patient.user != request.user:
            return redirect('home')
    elif hasattr(request.user, 'doctor_profile'):
        if appointment.doctor.user != request.user:
            return redirect('home')
    else:
        return redirect('home')
    
    context = {'appointment': appointment}
    return render(request, 'appointments/detail.html', context)


@login_required
def my_appointments(request):
    """View all patient appointments"""
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'appointments/my_appointments.html', context)


@login_required
def doctor_appointments(request):
    """View doctor's appointments"""
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'appointments/doctor_appointments.html', context)


@login_required
def approve_appointment(request, appointment_id):
    """Doctor approves an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if appointment.doctor != doctor:
        return redirect('home')
    
    if request.method == 'POST':
        appointment.status = 'approved'
        appointment.approved_date = timezone.now()
        appointment.save()
        # Send email notification to patient
        return redirect('appointments:doctor_appointments')
    
    context = {'appointment': appointment}
    return render(request, 'appointments/approve.html', context)


@login_required
def reject_appointment(request, appointment_id):
    """Doctor rejects an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if appointment.doctor != doctor:
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentRejectForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'rejected'
            appointment.rejected_date = timezone.now()
            appointment.save()
            # Send email notification to patient
            return redirect('appointments:doctor_appointments')
    else:
        form = AppointmentRejectForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointments/reject.html', context)


@login_required
def cancel_appointment(request, appointment_id):
    """Patient cancels an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = get_object_or_404(Patient, user=request.user)
    
    if appointment.patient != patient:
        return redirect('home')
    
    if appointment.status not in ['pending', 'approved']:
        return redirect('appointments:my_appointments')
    
    if request.method == 'POST':
        form = AppointmentRejectForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = 'cancelled'
            appointment.save()
            return redirect('appointments:my_appointments')
    else:
        form = AppointmentRejectForm(instance=appointment)
    
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointments/cancel.html', context)
