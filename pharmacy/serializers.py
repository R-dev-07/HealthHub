from rest_framework import serializers
from .models import Medicine, MedicineOrder, MedicineOrderItem, Pharmacist


class MedicineSerializer(serializers.ModelSerializer):
    in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Medicine
        fields = ('id', 'name', 'generic_name', 'category', 'price', 'stock_quantity',
                  'requires_prescription', 'dosage', 'manufacturer', 'is_available', 'in_stock')
        read_only_fields = ('id',)
    
    def get_in_stock(self, obj):
        return obj.is_in_stock()


class MedicineOrderItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    
    class Meta:
        model = MedicineOrderItem
        fields = ('id', 'medicine_name', 'quantity', 'unit_price')
        read_only_fields = ('id',)


class MedicineOrderSerializer(serializers.ModelSerializer):
    items = MedicineOrderItemSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = MedicineOrder
        fields = ('id', 'patient_name', 'items', 'total_amount', 'status', 'order_date',
                  'delivery_date', 'created_at')
        read_only_fields = ('id', 'order_date', 'created_at')


class PharmacistSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Pharmacist
        fields = ('id', 'user_name', 'license_number', 'qualification',
                  'years_of_experience', 'is_verified', 'created_at')
        read_only_fields = ('id', 'created_at')
