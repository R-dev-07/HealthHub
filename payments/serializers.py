from rest_framework import serializers
from .models import Payment, RefundRequest


class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = ('id', 'transaction_id', 'patient_name', 'payment_type', 'amount',
                  'status', 'payment_method', 'created_at', 'paid_at')
        read_only_fields = ('id', 'transaction_id', 'created_at', 'paid_at')


class RefundRequestSerializer(serializers.ModelSerializer):
    payment_info = PaymentSerializer(source='payment', read_only=True)
    
    class Meta:
        model = RefundRequest
        fields = ('id', 'payment_info', 'requested_amount', 'reason', 'status',
                  'requested_at', 'processed_at')
        read_only_fields = ('id', 'requested_at', 'processed_at')
