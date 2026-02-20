from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Patient, PatientReview
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified')
    list_filter = ('role', 'is_verified', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'date_of_birth', 'gender',
                                        'address', 'city', 'country', 'profile_image',
                                        'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'blood_group', 'created_at')
    list_filter = ('blood_group', 'created_at')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Patient Name'


@admin.register(PatientReview)
class PatientReviewAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'get_doctor_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name')
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
    
    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()
    get_doctor_name.short_description = 'Doctor'
