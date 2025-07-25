from django import forms
from .models import Product, Address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        labels = {
            'id': 'Product ID',
            'name': 'Name',
            'sku': 'SKU',
            'price': 'Price',
            'quantity': 'Quantity',
            'supplier': 'Supplier',
        }

        widgets = {
            'id': forms.NumberInput(attrs={'placeholder':'e.g. 1', 'class':'form-control'}),
            'name': forms.TextInput(attrs={'placeholder':'e.g. shirt', 'class':'form-control'}),
            'sku': forms.TextInput(attrs={'placeholder':'e.g. S12345', 'class':'form-control'}),
            'price': forms.NumberInput(attrs={'placeholder':'e.g. 19.99', 'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'placeholder':'e.g. 10', 'class':'form-control'}),
            'supplier': forms.TextInput(attrs={'placeholder':'e.g. ABC Corp', 'class':'form-control'}),
        }

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="E-mail")
    whatsapp_number = forms.CharField(required=False, label="WhatsApp")

    class Meta:
        model = User
        fields = ['username', 'email']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['cep', 'street', 'neighborhood', 'city', 'state', 'number', 'complement']