from django.db import models
from django.core.validators import RegexValidator
from patients.models import CustomUser


class Hospital(models.Model):
    """Hospital model"""
    name = models.CharField(max_length=200)
    admin_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,
                                    related_name='administered_hospitals')
    email = models.EmailField()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Invalid phone number.')
    phone = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='hospital_logos/', null=True, blank=True)
    description = models.TextField(blank=True)
    bed_capacity = models.IntegerField(null=True, blank=True)
    ambulance_facility = models.BooleanField(default=False)
    emergency_service = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Hospitals'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Department(models.Model):
    """Hospital departments"""
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('dermatology', 'Dermatology'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('general', 'General Medicine'),
        ('gastroenterology', 'Gastroenterology'),
        ('oncology', 'Oncology'),
        ('urology', 'Urology'),
        ('pathology', 'Pathology'),
        ('radiology', 'Radiology'),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    description = models.TextField(blank=True)
    head_of_department = models.CharField(max_length=100, blank=True)
    total_beds = models.IntegerField(default=0)
    available_beds = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Departments'
        unique_together = ('hospital', 'name')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_name_display()} - {self.hospital.name}"


class HospitalService(models.Model):
    """Hospital services"""
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Hospital Services'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"


class HospitalFacility(models.Model):
    """Hospital facilities"""
    FACILITY_CHOICES = [
        ('24hr_emergency', '24-Hour Emergency'),
        ('icu', 'ICU'),
        ('ot', 'Operation Theater'),
        ('ambulance', 'Ambulance Service'),
        ('pharmacy', 'In-house Pharmacy'),
        ('lab', 'Laboratory'),
        ('imaging', 'Imaging Center'),
        ('blood_bank', 'Blood Bank'),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='facilities')
    facility = models.CharField(max_length=50, choices=FACILITY_CHOICES)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Hospital Facilities'
        unique_together = ('hospital', 'facility')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_facility_display()} - {self.hospital.name}"
