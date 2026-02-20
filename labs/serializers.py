from rest_framework import serializers
from .models import LabTest, LabReport, LabTestOrder


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ('id', 'name', 'category', 'description', 'price', 'normal_range',
                  'sample_required', 'turnaround_time', 'is_active')
        read_only_fields = ('id',)


class LabReportSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = LabReport
        fields = ('id', 'test_name', 'patient_name', 'result_value', 'normal_range',
                  'status', 'test_date', 'completion_date', 'created_at')
        read_only_fields = ('id', 'created_at')


class LabTestOrderSerializer(serializers.ModelSerializer):
    tests = LabTestSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = LabTestOrder
        fields = ('id', 'tests', 'patient_name', 'total_cost', 'status', 'order_date',
                  'sample_collection_date', 'completion_date', 'created_at')
        read_only_fields = ('id', 'order_date', 'created_at')
