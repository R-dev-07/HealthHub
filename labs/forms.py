from django import forms
from .models import LabTest, LabReport


class LabTestSelectionForm(forms.Form):
    """Form to select lab tests"""
    tests = forms.ModelMultipleChoiceField(
        queryset=LabTest.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ('test', 'result_value', 'normal_range', 'remarks', 'pdf_report')
        widgets = {
            'test': forms.Select(attrs={'class': 'form-control'}),
            'result_value': forms.TextInput(attrs={'class': 'form-control'}),
            'normal_range': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pdf_report': forms.FileInput(attrs={'class': 'form-control'}),
        }
