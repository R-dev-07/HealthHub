from django import forms
from .models import Hospital, Department, HospitalService


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ('name', 'email', 'phone', 'address', 'city', 'country', 'website',
                  'logo', 'description', 'bed_capacity', 'ambulance_facility',
                  'emergency_service')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'bed_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'ambulance_facility': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'emergency_service': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'description', 'head_of_department', 'total_beds', 'available_beds')
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head_of_department': forms.TextInput(attrs={'class': 'form-control'}),
            'total_beds': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_beds': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class HospitalServiceForm(forms.ModelForm):
    class Meta:
        model = HospitalService
        fields = ('name', 'description', 'cost')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
