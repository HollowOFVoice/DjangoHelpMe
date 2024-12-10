from django import forms

from .models import Request, SimpleUser


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = SimpleUser
        fields = ['username', 'first_name', 'last_name','middle_name', 'email', 'password']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['address', 'contact_info', 'service_name', 'service_description', 'date', 'time', 'payment_type']

