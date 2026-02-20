from rest_framework import serializers
from .models import Hospital, Department, HospitalService, HospitalFacility


class HospitalSerializer(serializers.ModelSerializer):
    total_departments = serializers.SerializerMethodField()
    
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'email', 'phone', 'address', 'city', 'country',
                  'website', 'description', 'is_verified', 'total_departments', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_total_departments(self, obj):
        return obj.departments.count()


class DepartmentSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = Department
        fields = ('id', 'hospital_name', 'name', 'description', 'head_of_department',
                  'total_beds', 'available_beds', 'created_at')
        read_only_fields = ('id', 'created_at')


class HospitalServiceSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = HospitalService
        fields = ('id', 'hospital_name', 'name', 'description', 'cost', 'created_at')
        read_only_fields = ('id', 'created_at')


class HospitalFacilitySerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = HospitalFacility
        fields = ('id', 'hospital_name', 'facility', 'available', 'created_at')
        read_only_fields = ('id', 'created_at')
