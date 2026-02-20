from django.db import models
from django.core.validators import FileExtensionValidator
from patients.models import CustomUser


class Doctor(models.Model):
    """Doctor profile model"""
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('general', 'General Practice'),
        ('gastroenterology', 'Gastroenterology'),
        ('oncology', 'Oncology'),
        ('urology', 'Urology'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    registration_number = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.TextField()
    years_of_experience = models.IntegerField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    bio = models.TextField(blank=True)
    certificate = models.FileField(
        upload_to='doctor_certificates/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    availability_start = models.TimeField(null=True, blank=True)
    availability_end = models.TimeField(null=True, blank=True)
    working_days = models.CharField(
        max_length=50,
        default='Monday,Tuesday,Wednesday,Thursday,Friday',
        help_text="Comma-separated list of working days"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Doctors'
        ordering = ['-created_at']

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.get_specialization_display()})"

    def get_average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([r.rating for r in reviews]) / reviews.count()
        return 0


class DoctorHospitalRegistration(models.Model):
    """Track doctor registrations with hospitals"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='hospital_registrations')
    hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('doctor', 'hospital')
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.hospital.name} ({self.get_status_display()})"


class Prescription(models.Model):
    """Prescription model"""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='prescriptions')
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.SET_NULL, 
                                       null=True, blank=True, related_name='prescription')
    medicines = models.TextField(help_text="List of medicines prescribed")
    dosage = models.TextField()
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Prescriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Prescription for {self.patient.user.get_full_name()} by Dr. {self.doctor.user.get_full_name()}"
