from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUser(AbstractUser):
    """Custom User model for the platform"""
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('hospital_admin', 'Hospital Admin'),
        ('lab_worker', 'Lab Worker'),
        ('pharmacist', 'Pharmacist'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Enter a valid phone number.'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        null=True,
        blank=True
    )
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"


class Patient(models.Model):
    """Patient profile model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    blood_group = models.CharField(
        max_length=5,
        choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        blank=True
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=17, blank=True)
    allergies = models.TextField(blank=True, help_text="List any allergies")
    medical_history = models.TextField(blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Patients'
        ordering = ['-created_at']

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"


class PatientReview(models.Model):
    """Patient reviews for doctors"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_reviews')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 rating
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Patient Reviews'
        ordering = ['-created_at']
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"Review by {self.patient.user.get_full_name()} for {self.doctor.user.get_full_name()}"
