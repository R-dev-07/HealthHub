from rest_framework import serializers
from .models import Doctor, DoctorHospitalRegistration, Prescription


class DoctorSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ('id', 'user_name', 'specialization', 'registration_number', 
                  'consultation_fee', 'bio', 'years_of_experience', 'is_verified',
                  'average_rating', 'created_at')
        read_only_fields = ('id', 'is_verified', 'created_at')
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()


class PrescriptionSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = Prescription
        fields = ('id', 'doctor_name', 'patient_name', 'medicines', 'dosage',
                  'duration', 'instructions', 'created_at')
        read_only_fields = ('id', 'created_at')


class DoctorHospitalRegistrationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = DoctorHospitalRegistration
        fields = ('id', 'doctor_name', 'hospital_name', 'status', 'applied_date', 'approved_date')
        read_only_fields = ('id', 'applied_date', 'approved_date')
