from django import forms
from django.utils import timezone
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('appointment_date', 'reason_for_visit')
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'reason_for_visit': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your symptoms or reason for visit'
            }),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < timezone.now():
            raise forms.ValidationError('Appointment date must be in the future.')
        return appointment_date


class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class AppointmentRejectForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('cancellation_reason',)
        widgets = {
            'cancellation_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'label': 'Rejection Reason'
            }),
        }
