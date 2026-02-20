from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LabTest, LabReport, LabTestOrder
from .serializers import LabTestSerializer, LabReportSerializer, LabTestOrderSerializer
from .forms import LabTestSelectionForm, LabReportForm
from patients.models import Patient


# API Views
class LabTestViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Lab Tests"""
    queryset = LabTest.objects.filter(is_active=True)
    serializer_class = LabTestSerializer
    permission_classes = [IsAuthenticated]


class LabReportViewSet(viewsets.ModelViewSet):
    """API ViewSet for Lab Reports"""
    queryset = LabReport.objects.all()
    serializer_class = LabReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient_profile'):
            return LabReport.objects.filter(patient=user.patient_profile)
        elif user.role == 'lab_worker':
            return LabReport.objects.all()
        return LabReport.objects.none()


# Function-based Views
def lab_tests(request):
    """List all available lab tests"""
    tests = LabTest.objects.filter(is_active=True)
    category_filter = request.GET.get('category', '')
    
    if category_filter:
        tests = tests.filter(category=category_filter)
    
    context = {
        'tests': tests,
        'category_filter': category_filter,
        'categories': LabTest.TEST_CATEGORIES,
    }
    return render(request, 'labs/tests_list.html', context)


@login_required
def select_lab_tests(request):
    """Patient selects lab tests"""
    patient = get_object_or_404(Patient, user=request.user)
    
    if request.method == 'POST':
        form = LabTestSelectionForm(request.POST)
        if form.is_valid():
            tests = form.cleaned_data['tests']
            total_cost = sum([test.price for test in tests])
            
            # Create lab test order
            order = LabTestOrder.objects.create(
                patient=patient,
                total_cost=total_cost
            )
            order.tests.set(tests)
            
            return redirect('labs:proceed_to_payment', order_id=order.id)
    else:
        form = LabTestSelectionForm()
    
    context = {'form': form}
    return render(request, 'labs/select_tests.html', context)


@login_required
def patient_lab_orders(request):
    """View patient's lab orders"""
    patient = get_object_or_404(Patient, user=request.user)
    orders = patient.lab_test_orders.all().order_by('-created_at')
    
    context = {'orders': orders}
    return render(request, 'labs/my_orders.html', context)


@login_required
def patient_lab_reports(request):
    """View patient's lab reports"""
    patient = get_object_or_404(Patient, user=request.user)
    reports = patient.lab_reports.all().order_by('-created_at')
    
    context = {'reports': reports}
    return render(request, 'labs/my_reports.html', context)


@login_required
def lab_worker_dashboard(request):
    """Lab worker dashboard"""
    if request.user.role != 'lab_worker':
        return redirect('home')
    
    pending_orders = LabTestOrder.objects.filter(status='sample_collected')
    completed_orders = LabTestOrder.objects.filter(status='completed').count()
    total_tests_processed = LabReport.objects.filter(lab_worker=request.user).count()
    
    context = {
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_tests_processed': total_tests_processed,
    }
    return render(request, 'labs/worker_dashboard.html', context)


@login_required
def upload_lab_report(request, order_id):
    """Lab worker uploads report"""
    if request.user.role != 'lab_worker':
        return redirect('home')
    
    order = get_object_or_404(LabTestOrder, id=order_id)
    
    if request.method == 'POST':
        form = LabReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = order.patient
            report.lab_worker = request.user
            report.save()
            
            order.status = 'completed'
            order.save()
            
            return redirect('labs:worker_dashboard')
    else:
        form = LabReportForm()
    
    context = {'form': form, 'order': order}
    return render(request, 'labs/upload_report.html', context)
