from django import forms
from .models import Payment, RefundRequest


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_method', 'notes')
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = ('requested_amount', 'reason')
        widgets = {
            'requested_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
