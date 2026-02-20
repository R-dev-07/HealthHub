from django.db import models
from patients.models import Patient, CustomUser


class LabTest(models.Model):
    """Available laboratory tests"""
    TEST_CATEGORIES = [
        ('blood', 'Blood Tests'),
        ('urine', 'Urine Tests'),
        ('imaging', 'Imaging Tests'),
        ('pathology', 'Pathology Tests'),
        ('other', 'Other Tests'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=TEST_CATEGORIES)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    normal_range = models.CharField(max_length=200, blank=True)
    sample_required = models.CharField(max_length=100, blank=True)
    turnaround_time = models.CharField(max_length=100, help_text="e.g., '24 hours'")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Lab Tests'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class LabReport(models.Model):
    """Patient lab reports"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_reports')
    lab_worker = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    limit_choices_to={'role': 'lab_worker'})
    test = models.ForeignKey(LabTest, on_delete=models.SET_NULL, null=True)
    result_value = models.CharField(max_length=200, blank=True)
    normal_range = models.CharField(max_length=200, blank=True)
    remarks = models.TextField(blank=True)
    pdf_report = models.FileField(upload_to='lab_reports/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    test_date = models.DateTimeField()
    completion_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Lab Reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test.name} - {self.patient.user.get_full_name()}"


class LabTestOrder(models.Model):
    """Lab test orders from patients"""
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('sample_collected', 'Sample Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_test_orders')
    tests = models.ManyToManyField(LabTest, related_name='orders')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    payment_id = models.CharField(max_length=100, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    sample_collection_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Lab Test Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Lab Order #{self.id} - {self.patient.user.get_full_name()}"
