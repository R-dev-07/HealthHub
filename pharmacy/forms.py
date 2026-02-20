from django import forms
from .models import Medicine, MedicineOrder, MedicineOrderItem


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ('name', 'generic_name', 'category', 'description', 'price',
                  'stock_quantity', 'requires_prescription', 'dosage', 'side_effects',
                  'manufacturer', 'expiry_date', 'is_available')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'requires_prescription': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'side_effects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MedicineOrderForm(forms.ModelForm):
    class Meta:
        model = MedicineOrder
        fields = ('delivery_address', 'notes')
        widgets = {
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AddToCartForm(forms.Form):
    """Form to add medicine to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'value': 1})
    )
