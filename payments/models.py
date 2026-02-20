from django.db import models
from patients.models import Patient


class Payment(models.Model):
    """Payment model for all transactions"""
    PAYMENT_TYPE_CHOICES = [
        ('appointment', 'Appointment'),
        ('lab_test', 'Lab Test'),
        ('medicine', 'Medicine'),
        ('service', 'Service'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('debit_card', 'Debit Card'),
            ('credit_card', 'Credit Card'),
            ('mobile_banking', 'Mobile Banking'),
            ('bank_transfer', 'Bank Transfer'),
            ('wallet', 'Wallet'),
        ]
    )
    gateway_response = models.JSONField(null=True, blank=True)
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='payment')
    lab_test_order = models.OneToOneField('labs.LabTestOrder', on_delete=models.SET_NULL,
                                          null=True, blank=True, related_name='payment')
    medicine_order = models.OneToOneField('pharmacy.MedicineOrder', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='payment')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.transaction_id} - {self.patient.user.get_full_name()}"

    def is_paid(self):
        return self.status == 'completed'


class PaymentGatewayConfig(models.Model):
    """Configuration for payment gateway"""
    name = models.CharField(max_length=50, unique=True)  # e.g., 'SSLCommerz'
    store_id = models.CharField(max_length=100)
    store_password = models.CharField(max_length=100)
    is_sandbox = models.BooleanField(default=True)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Payment Gateway Configs'

    def __str__(self):
        return f"{self.name} ({['Live', 'Sandbox'][self.is_sandbox]})"


class RefundRequest(models.Model):
    """Refund requests"""
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]
    
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='refund_request')
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Refund Requests'
        ordering = ['-requested_at']

    def __str__(self):
        return f"Refund Request for Payment #{self.payment.transaction_id}"
