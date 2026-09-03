from django import forms
from .models import Customer, Invoice

TAILWIND_INPUT = 'w-full border border-gray-300 rounded-lg p-2.5 bg-white outline-none focus:border-red-600 focus:ring-1 focus:ring-red-600 transition'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'mobile', 'address', 'aadhar_no']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'e.g. Ramesh Kumar',
                'id': 'cust_name',
            }),
            'mobile': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'e.g. 9876543210',
                'maxlength': '15',
                'id': 'cust_mobile',
            }),
            'address': forms.Textarea(attrs={
                'class': TAILWIND_INPUT,
                'rows': 2,
                'placeholder': 'Village / Ward, District, State',
                'id': 'cust_address',
            }),
            'aadhar_no': forms.TextInput(attrs={
                'class': TAILWIND_INPUT,
                'placeholder': 'e.g. 1234 5678 9012 (optional)',
                'maxlength': '20',
                'id': 'cust_aadhar',
            }),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = []


