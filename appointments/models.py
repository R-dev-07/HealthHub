from django.db import models
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    """Appointment model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.SET_NULL, null=True)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    consultation_notes = models.TextField(blank=True)
    reason_for_visit = models.TextField()
    is_paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True)
    cancellation_reason = models.TextField(blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejected_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date']
        unique_together = ('doctor', 'appointment_date', 'patient')

    def __str__(self):
        return f"Appointment: {self.patient.user.get_full_name()} with Dr. {self.doctor.user.get_full_name()}"

    def is_upcoming(self):
        """Check if appointment is upcoming"""
        return self.appointment_date > timezone.now()

    def is_overdue(self):
        """Check if appointment is overdue"""
        return self.appointment_date < timezone.now() and self.status != 'completed'

    @property
    def duration_minutes(self):
        return 30  # Default appointment duration
