from django.contrib import admin
from .models import Doctor, DoctorHospitalRegistration, Prescription


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'specialization', 'is_verified', 'consultation_fee', 'created_at')
    list_filter = ('specialization', 'is_verified', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'registration_number')
    fieldsets = (
        ('User Information', {'fields': ('user',)}),
        ('Professional Details', {'fields': ('specialization', 'registration_number', 'license_number',
                                              'qualification', 'years_of_experience')}),
        ('Consultation', {'fields': ('consultation_fee', 'bio')}),
        ('Availability', {'fields': ('availability_start', 'availability_end', 'working_days')}),
        ('Verification', {'fields': ('certificate', 'is_verified', 'verification_date')}),
    )
    
    def get_name(self, obj):
        return f"Dr. {obj.user.get_full_name()}"
    get_name.short_description = 'Doctor Name'


@admin.register(DoctorHospitalRegistration)
class DoctorHospitalRegistrationAdmin(admin.ModelAdmin):
    list_display = ('get_doctor_name', 'hospital', 'status', 'applied_date')
    list_filter = ('status', 'applied_date', 'hospital')
    search_fields = ('doctor__user__first_name', 'hospital__name')
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('get_doctor_name', 'get_patient_name', 'created_at')
    list_filter = ('created_at', 'doctor')
    search_fields = ('doctor__user__first_name', 'patient__user__first_name')
    
    def get_doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.get_full_name()}"
    get_doctor_name.short_description = 'Doctor'
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
