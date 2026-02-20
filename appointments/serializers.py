from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.get_specialization_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ('id', 'patient_name', 'doctor_name', 'hospital_name', 'doctor_specialization',
                  'appointment_date', 'status', 'reason_for_visit', 'is_paid', 'created_at')
        read_only_fields = ('id', 'created_at')
