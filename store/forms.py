from django import forms
from .models import ShippingAddress, PaymentInfo

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['street', 'city', 'state', 'postal_code', 'country']

class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        fields = ['card_number', 'cardholder_name', 'expiration_date', 'cvv']