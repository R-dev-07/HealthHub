from django.contrib import admin
from .models import Medicine, MedicineOrder, MedicineOrderItem, Pharmacist


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'requires_prescription', 'created_at')
    search_fields = ('name', 'generic_name', 'manufacturer')
    fieldsets = (
        ('Medicine Information', {'fields': ('name', 'generic_name', 'category')}),
        ('Details', {'fields': ('dosage', 'description', 'side_effects')}),
        ('Pricing & Stock', {'fields': ('price', 'stock_quantity')}),
        ('Supplier Info', {'fields': ('manufacturer', 'requires_prescription', 'expiry_date')}),
        ('Status', {'fields': ('is_available',)}),
    )


@admin.register(MedicineOrder)
class MedicineOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient_name', 'total_amount', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('patient__user__first_name', 'id')
    
    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()
    get_patient_name.short_description = 'Patient'


@admin.register(MedicineOrderItem)
class MedicineOrderItemAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity', 'unit_price', 'order')
    list_filter = ('added_at',)
    search_fields = ('medicine__name', 'order__id')


@admin.register(Pharmacist)
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'license_number', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__first_name', 'license_number')
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = 'Pharmacist'
