from django import forms
from django.contrib.auth.models import User
from .models import Request


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['address', 'contact_number',  'date_time', 'payment_type']


