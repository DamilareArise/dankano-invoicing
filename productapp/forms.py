from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'price_per_Qty',
            'quantity',
            'unit'
        ]


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'client_name',
            'client_phone',
            'agent',
            'payment_method',
            'payment_status'
        ]


