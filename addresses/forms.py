from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'email',
            'phone_number',
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
            'phone_number' : "",
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
            "phone_number" : forms.TextInput(attrs={'placeholder':'Phone Number','name':'number','class':'email-input number-only','pattern':'[0-9]{10}'}),
            "first_name":forms.TextInput(attrs={'placeholder':'First Name','name':'first_name','class':'firstname-input text-only'}),
            "last_name":forms.TextInput(attrs={'placeholder':'Last Name','name':'last_name','class':'lastname-input text-only'}),
            "address_line_1":forms.TextInput(attrs={'placeholder':'Address','name':'address_line_1','class':'address-line-1-input'}),
            "address_line_2":forms.TextInput(attrs={'placeholder':'Apartment, flat number, etc.','name':'address_line_2','class':'address-line-2-input'}),
            "city":forms.TextInput(attrs={'placeholder':'City','name':'city','class':'city-input text-only'}),
            "state":forms.TextInput(attrs={'placeholder':'State','name':'state','class':'state-input text-only'}),
            "country":forms.TextInput(attrs={'placeholder':'Country','name':'country','class':'country-input text-only'}),
            "postal_code":forms.TextInput(attrs={'placeholder':'Pincode','name':'pincode','class':'pincode-input number-only','pattern':'[0-9]{6}'}),
        }
