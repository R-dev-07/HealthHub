from django.db import models
from django.core.validators import MinValueValidator
from patients.models import Patient, CustomUser


class Medicine(models.Model):
    """Medicine model"""
    CATEGORY_CHOICES = [
        ('antibiotic', 'Antibiotic'),
        ('painkiller', 'Painkiller'),
        ('antacid', 'Antacid'),
        ('cough_cold', 'Cough & Cold'),
        ('vitamin', 'Vitamin'),
        ('allergy', 'Allergy'),
        ('diabetes', 'Diabetes'),
        ('bp', 'Blood Pressure'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    requires_prescription = models.BooleanField(default=False)
    dosage = models.CharField(max_length=100, blank=True)
    side_effects = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Medicines'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock_quantity > 0


class MedicineOrder(models.Model):
    """Patient medicine orders"""
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicine_orders')
    medicines = models.ManyToManyField(Medicine, through='MedicineOrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    payment_id = models.CharField(max_length=100, blank=True)
    delivery_address = models.TextField(blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Medicine Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.patient.user.get_full_name()}"

    def calculate_total(self):
        """Calculate total from items"""
        return sum([item.get_subtotal() for item in self.items.all()])


class MedicineOrderItem(models.Model):
    """Individual medicine items in an order"""
    order = models.ForeignKey(MedicineOrder, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Medicine Order Items'
        unique_together = ('order', 'medicine')

    def __str__(self):
        return f"{self.medicine.name} x {self.quantity}"

    def get_subtotal(self):
        """Get subtotal for this item"""
        return self.quantity * self.unit_price


class Pharmacist(models.Model):
    """Pharmacist profile"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pharmacist_profile',
                                 limit_choices_to={'role': 'pharmacist'})
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=200)
    years_of_experience = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=17, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Pharmacists'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pharmacist: {self.user.get_full_name()}"
