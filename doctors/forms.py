from django import forms
from .models import Doctor, DoctorHospitalRegistration, Prescription


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('specialization', 'registration_number', 'license_number', 'qualification',
                  'years_of_experience', 'consultation_fee', 'bio', 'certificate',
                  'availability_start', 'availability_end', 'working_days')
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'certificate': forms.FileInput(attrs={'class': 'form-control'}),
            'availability_start': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'availability_end': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('medicines', 'dosage', 'duration', 'instructions')
        widgets = {
            'medicines': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'dosage': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DoctorHospitalRegistrationForm(forms.ModelForm):
    class Meta:
        model = DoctorHospitalRegistration
        fields = ('hospital',)
        widgets = {
            'hospital': forms.Select(attrs={'class': 'form-control'}),
        }
