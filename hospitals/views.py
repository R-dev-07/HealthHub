from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hospital, Department, HospitalService, HospitalFacility
from .serializers import HospitalSerializer, DepartmentSerializer, HospitalServiceSerializer
from .forms import HospitalForm, DepartmentForm, HospitalServiceForm


# API Views
class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Hospitals"""
    queryset = Hospital.objects.filter(is_verified=True)
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated]


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Departments"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        hospital_id = self.request.query_params.get('hospital_id', None)
        if hospital_id:
            return Department.objects.filter(hospital_id=hospital_id)
        return Department.objects.all()


# Function-based Views
def hospital_list(request):
    """List all hospitals"""
    hospitals = Hospital.objects.filter(is_verified=True)
    
    context = {'hospitals': hospitals}
    return render(request, 'hospitals/list.html', context)


def hospital_detail(request, hospital_id):
    """Hospital detail view"""
    hospital = get_object_or_404(Hospital, id=hospital_id, is_verified=True)
    departments = hospital.departments.all()
    services = hospital.services.all()
    facilities = hospital.facilities.all()
    
    context = {
        'hospital': hospital,
        'departments': departments,
        'services': services,
        'facilities': facilities,
    }
    return render(request, 'hospitals/detail.html', context)


def hospital_departments(request, hospital_id):
    """List hospital departments"""
    hospital = get_object_or_404(Hospital, id=hospital_id)
    departments = hospital.departments.all()
    
    context = {
        'hospital': hospital,
        'departments': departments,
    }
    return render(request, 'hospitals/departments.html', context)


@login_required
def hospital_admin_dashboard(request):
    """Hospital admin dashboard"""
    hospitals = None
    if hasattr(request.user, 'administered_hospitals'):
        hospitals = request.user.administered_hospitals.all()
    
    context = {'hospitals': hospitals}
    return render(request, 'hospitals/admin_dashboard.html', context)


@login_required
def create_hospital(request):
    """Create hospital (for admins)"""
    if request.method == 'POST':
        form = HospitalForm(request.POST, request.FILES)
        if form.is_valid():
            hospital = form.save(commit=False)
            hospital.admin_user = request.user
            hospital.save()
            return redirect('hospital_detail', hospital_id=hospital.id)
    else:
        form = HospitalForm()
    
    context = {'form': form}
    return render(request, 'hospitals/create.html', context)


@login_required
def edit_hospital(request, hospital_id):
    """Edit hospital"""
    hospital = get_object_or_404(Hospital, id=hospital_id, admin_user=request.user)
    
    if request.method == 'POST':
        form = HospitalForm(request.POST, request.FILES, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_detail', hospital_id=hospital.id)
    else:
        form = HospitalForm(instance=hospital)
    
    context = {'form': form, 'hospital': hospital}
    return render(request, 'hospitals/edit.html', context)


@login_required
def create_department(request, hospital_id):
    """Create department"""
    hospital = get_object_or_404(Hospital, id=hospital_id, admin_user=request.user)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.hospital = hospital
            department.save()
            return redirect('hospital_departments', hospital_id=hospital.id)
    else:
        form = DepartmentForm()
    
    context = {'form': form, 'hospital': hospital}
    return render(request, 'hospitals/create_department.html', context)


@login_required
def create_service(request, hospital_id):
    """Create hospital service"""
    hospital = get_object_or_404(Hospital, id=hospital_id, admin_user=request.user)
    
    if request.method == 'POST':
        form = HospitalServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.hospital = hospital
            service.save()
            return redirect('hospital_detail', hospital_id=hospital.id)
    else:
        form = HospitalServiceForm()
    
    context = {'form': form, 'hospital': hospital}
    return render(request, 'hospitals/create_service.html', context)
