from django import forms
from .models import Product

class ImportFileForm(forms.Form):
    file = forms.FileField(label='Select CSV or Excel file', widget=forms.FileInput(attrs={'class': 'form-file', 'accept': '.csv, .xlsx, .xls'}))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'purchase_price', 'selling_price', 'quantity', 'min_stock_alert', 'description', 'image', 'supplier_name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product Name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Barcode/Code'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'min_stock_alert': forms.NumberInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'supplier_name': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }
