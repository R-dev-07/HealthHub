import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import QuerySet
from .models import Payment, PaymentGatewayConfig, RefundRequest
from .serializers import PaymentSerializer, RefundRequestSerializer
from .forms import PaymentForm, RefundRequestForm
from patients.models import Patient


# API Views
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Payments"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[Payment]:
        user = self.request.user
        try:
            patient = Patient.objects.get(user=user)
            return Payment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            return Payment.objects.none()


class RefundRequestViewSet(viewsets.ModelViewSet):
    """API ViewSet for Refund Requests"""
    queryset = RefundRequest.objects.all()
    serializer_class = RefundRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self) -> QuerySet[RefundRequest]:
        user = self.request.user
        try:
            patient = Patient.objects.get(user=user)
            return RefundRequest.objects.filter(payment__patient=patient)
        except Patient.DoesNotExist:
            return RefundRequest.objects.none()


# Function-based Views
def initiate_payment(request, payment_type, object_id):
    """Initiate payment process"""
    patient = get_object_or_404(Patient, user=request.user)
    
    # Fetch the object to be paid for
    amount = 0
    appointment = None
    lab_test_order = None
    medicine_order = None
    
    if payment_type == 'appointment':
        from appointments.models import Appointment
        appointment = get_object_or_404(Appointment, id=object_id)
        amount = appointment.doctor.consultation_fee
    elif payment_type == 'lab_test':
        from labs.models import LabTestOrder
        lab_test_order = get_object_or_404(LabTestOrder, id=object_id)
        amount = lab_test_order.total_cost
    elif payment_type == 'medicine':
        from pharmacy.models import MedicineOrder
        medicine_order = get_object_or_404(MedicineOrder, id=object_id)
        amount = medicine_order.total_amount
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                patient=patient,
                transaction_id=f"TXN{patient.id}{object_id}{timezone.now().timestamp()}",
                payment_type=payment_type,
                amount=amount,
                payment_method=form.cleaned_data['payment_method'],
                notes=form.cleaned_data['notes'],
                appointment=appointment,
                lab_test_order=lab_test_order,
                medicine_order=medicine_order,
            )
            
            payment.status = 'processing'
            payment.save()
            
            return redirect('payments:payment_gateway', payment_id=payment.id)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'payment_type': payment_type,
        'amount': amount,
    }
    return render(request, 'payments/initiate.html', context)


@login_required
def payment_gateway(request, payment_id):
    """Payment gateway page (SSLCommerz integration)"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.patient.user != request.user:
        return redirect('home')
    
    # Get SSLCommerz config
    try:
        gateway_config = PaymentGatewayConfig.objects.get(name='SSLCommerz', is_active=True)
    except PaymentGatewayConfig.DoesNotExist:
        return render(request, 'payments/error.html', 
                      {'error': 'Payment gateway is not configured'})
    
    # Create SSLCommerz payment request
    sslcommerz_data = {
        'store_id': gateway_config.store_id,
        'store_passwd': gateway_config.store_password,
        'total_amount': str(payment.amount),
        'currency': 'BDT',
        'tran_id': payment.transaction_id,
        'success_url': request.build_absolute_uri('/payments/success/'),
        'fail_url': request.build_absolute_uri('/payments/failed/'),
        'cancel_url': request.build_absolute_uri('/payments/cancelled/'),
        'client_ip': request.META.get('REMOTE_ADDR'),
        'cus_name': request.user.get_full_name(),
        'cus_email': request.user.email,
        'cus_phone': payment.patient.user.phone_number,
        'shipping_method': 'NO',
        'product_name': f"{payment.payment_type} - {payment.transaction_id}",
        'product_category': payment.payment_type,
        'product_profile': 'medical_service',
    }
    
    context = {
        'payment': payment,
        'gateway_config': gateway_config,
        'sslcommerz_data': sslcommerz_data,
    }
    return render(request, 'payments/gateway.html', context)


@require_POST
def payment_success(request):
    """Handle successful payment"""
    transaction_id = request.POST.get('tran_id')
    
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.gateway_response = dict(request.POST)
        payment.save()
        
        # Update related object status
        if payment.appointment:
            payment.appointment.is_paid = True
            payment.appointment.save()
        elif payment.lab_test_order:
            payment.lab_test_order.status = 'paid'
            payment.lab_test_order.payment_id = transaction_id
            payment.lab_test_order.save()
        elif payment.medicine_order:
            payment.medicine_order.status = 'paid'
            payment.medicine_order.payment_id = transaction_id
            payment.medicine_order.save()
        
        return render(request, 'payments/success.html', {'payment': payment})
    except Payment.DoesNotExist:
        return render(request, 'payments/error.html', {'error': 'Payment not found'})


@require_POST
def payment_failed(request):
    """Handle failed payment"""
    transaction_id = request.POST.get('tran_id')
    
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = 'failed'
        payment.gateway_response = dict(request.POST)
        payment.save()
        
        return render(request, 'payments/failed.html', {'payment': payment})
    except Payment.DoesNotExist:
        return render(request, 'payments/error.html', {'error': 'Payment not found'})


@require_POST
def payment_cancelled(request):
    """Handle cancelled payment"""
    transaction_id = request.POST.get('tran_id')
    
    try:
        payment = Payment.objects.get(transaction_id=transaction_id)
        payment.status = 'pending'
        payment.gateway_response = dict(request.POST)
        payment.save()
        
        return render(request, 'payments/cancelled.html', {'payment': payment})
    except Payment.DoesNotExist:
        return render(request, 'payments/error.html', {'error': 'Payment not found'})


@login_required
def payment_history(request):
    """View payment history"""
    patient = get_object_or_404(Patient, user=request.user)
    payments = patient.payments.all().order_by('-created_at')
    
    context = {'payments': payments}
    return render(request, 'payments/history.html', context)


@login_required
def request_refund(request, payment_id):
    """Request refund for a payment"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if payment.patient.user != request.user:
        return redirect('home')
    
    if not payment.is_paid():
        return render(request, 'payments/error.html', {'error': 'Only paid payments can be refunded'})
    
    try:
        refund_request = RefundRequest.objects.get(payment=payment)
        return redirect('payments:refund_detail', refund_id=refund_request.id)
    except RefundRequest.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            refund_request = form.save(commit=False)
            refund_request.payment = payment
            refund_request.save()
            return redirect('payments:refund_detail', refund_id=refund_request.id)
    else:
        form = RefundRequestForm(initial={'requested_amount': payment.amount})
    
    context = {
        'form': form,
        'payment': payment,
    }
    return render(request, 'payments/request_refund.html', context)


@login_required
def refund_detail(request, refund_id):
    """View refund request details"""
    refund_request = get_object_or_404(RefundRequest, id=refund_id)
    
    if refund_request.payment.patient.user != request.user:
        return redirect('home')
    
    context = {'refund_request': refund_request}
    return render(request, 'payments/refund_detail.html', context)
