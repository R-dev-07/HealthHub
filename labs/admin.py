from django.contrib import admin
from .models import LabTest, LabReport, LabTestOrder


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('get_test_name', 'get_patient_name', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'test')
    search_fields = ('patient__user__first_name', 'test__name')
    
    def get_test_name(self, obj):
        return obj.test.name if obj.test else 'N/A'
    get_test_name.short_description = 'Test'
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'


@admin.register(LabTestOrder)
class LabTestOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient_name', 'total_cost', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__user__first_name', 'id')
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'
