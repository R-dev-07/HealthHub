from django.contrib import admin
from .models import Payment, PaymentGatewayConfig, RefundRequest


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'get_patient_name', 'amount', 'payment_type', 'status', 'created_at')
    list_filter = ('status', 'payment_type', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'patient__user__first_name')
    fieldsets = (
        ('Transaction Info', {'fields': ('transaction_id', 'patient', 'amount')}),
        ('Payment Details', {'fields': ('payment_type', 'payment_method', 'status')}),
        ('Related Objects', {'fields': ('appointment', 'lab_test_order', 'medicine_order')}),
        ('Gateway Info', {'fields': ('gateway_response', 'notes')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'paid_at')}),
    )
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'


@admin.register(PaymentGatewayConfig)
class PaymentGatewayConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_sandbox', 'is_active', 'updated_at')
    list_filter = ('is_sandbox', 'is_active')
    fieldsets = (
        ('Gateway Info', {'fields': ('name', 'api_url', 'is_sandbox', 'is_active')}),
        ('Credentials', {'fields': ('store_id', 'store_password')}),
    )


@admin.register(RefundRequest)
class RefundRequestAdmin(admin.ModelAdmin):
    list_display = ('payment', 'requested_amount', 'status', 'requested_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('payment__transaction_id', 'reason')
