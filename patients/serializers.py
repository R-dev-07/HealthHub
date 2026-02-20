from rest_framework import serializers
from .models import CustomUser, Patient, PatientReview


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'role', 'profile_image', 'is_verified')
        read_only_fields = ('id', 'is_verified')


class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ('id', 'user', 'blood_group', 'emergency_contact_name',
                  'emergency_contact_number', 'allergies', 'medical_history',
                  'height', 'weight', 'created_at')
        read_only_fields = ('id', 'created_at')


class PatientReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    
    class Meta:
        model = PatientReview
        fields = ('id', 'patient_name', 'doctor_name', 'rating', 'review_text', 'created_at')
        read_only_fields = ('id', 'created_at')
