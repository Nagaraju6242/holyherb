from django import forms
from .models import ShippingMethod

class ShippingMethodForm(forms.ModelForm):
    class Meta:
        model = ShippingMethod
        fields = [
            'email',
            'first_name',
            'last_name',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'postal_code'
        ]
        labels = {
            'email' : "",
            'first_name' : "",
            'last_name' : "",
            'address_line_1' : "",
            'address_line_2' : "",
            'city' : "",
            'state' : "",
            'country' : "",
            'postal_code' : ""
        }
        widgets = {
            "email":forms.EmailInput(attrs={'placeholder':'Email Address','name':'email','class':'email-input'}),
            "first_name":forms.TextInput(attrs={'placeholder':'First Name','name':'first_name','class':'firstname-input'}),
            "last_name":forms.TextInput(attrs={'placeholder':'Last Name','name':'last_name','class':'lastname-input'}),
            "address_line_1":forms.TextInput(attrs={'placeholder':'Address','name':'address_line_1','class':'address-line-1-input'}),
            "address_line_2":forms.TextInput(attrs={'placeholder':'Apartment, flat number, etc.','name':'address_line_2','class':'address-line-2-input'}),
            "city":forms.TextInput(attrs={'placeholder':'City','name':'city','class':'city-input'}),
            "state":forms.TextInput(attrs={'placeholder':'State','name':'state','class':'state-input'}),
            "country":forms.TextInput(attrs={'placeholder':'Country','name':'country','class':'country-input'}),
            "postal_code":forms.TextInput(attrs={'placeholder':'Pincode','name':'pincode','class':'pincode-input'}),
        }