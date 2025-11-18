# billing/forms.py
from django import forms
from .models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['amount', 'payment_status', 'payment_date', 'handled_by']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'handled_by': forms.Select(attrs={'class': 'form-select'}),
        }
