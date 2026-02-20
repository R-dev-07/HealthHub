from django.contrib import admin
from .models import Hospital, Department, HospitalService, HospitalFacility


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'city', 'created_at')
    search_fields = ('name', 'city', 'email')
    fieldsets = (
        ('Hospital Information', {'fields': ('name', 'admin_user', 'email', 'phone')}),
        ('Location', {'fields': ('address', 'city', 'country')}),
        ('Details', {'fields': ('website', 'logo', 'description', 'bed_capacity')}),
        ('Facilities', {'fields': ('ambulance_facility', 'emergency_service')}),
        ('Verification', {'fields': ('is_verified',)}),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'hospital', 'total_beds', 'available_beds')
    list_filter = ('name', 'hospital', 'created_at')
    search_fields = ('hospital__name', 'name')
    
    def get_name(self, obj):
        return obj.get_name_display()
    get_name.short_description = 'Department'


@admin.register(HospitalService)
class HospitalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'hospital', 'cost', 'created_at')
    list_filter = ('hospital', 'created_at')
    search_fields = ('name', 'hospital__name')


@admin.register(HospitalFacility)
class HospitalFacilityAdmin(admin.ModelAdmin):
    list_display = ('get_facility', 'hospital', 'available')
    list_filter = ('facility', 'hospital', 'available')
    search_fields = ('hospital__name', 'facility')
    
    def get_facility(self, obj):
        return obj.get_facility_display()
    get_facility.short_description = 'Facility'
