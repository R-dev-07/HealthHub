from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'appointment_date', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'appointment_date', 'created_at')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    fieldsets = (
        ('Appointment Information', {'fields': ('patient', 'doctor', 'hospital', 'appointment_date')}),
        ('Visit Details', {'fields': ('reason_for_visit', 'consultation_notes')}),
        ('Status', {'fields': ('status', 'cancellation_reason')}),
        ('Payment', {'fields': ('is_paid', 'payment_id')}),
        ('Dates', {'fields': ('approved_date', 'rejected_date', 'completion_date')}),
    )
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'
