from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from main.models import Request


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Проверка на пустые поля
        if not username:
            raise ValidationError("Логин не может быть пустым.")
        if not password:
            raise ValidationError("Пароль не может быть пустым.")

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError("Неверный логин или пароль.")

        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        # Проверяем, что пароли совпадают
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Пароли не совпадают.")

        # Проверка пароля
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(f"Пароль не удовлетворяет требованиям: {e.messages}")

        # Валидация email (проверка уникальности и правильности формата)
        if email and get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже зарегистрирован.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['address', 'service', 'preferred_date_time', 'payment_type']
        labels = {
            'address': 'Адрес',
            'service': 'Услуга',
            'preferred_date_time': 'Дата и время',
            'payment_type': 'Тип оплаты',
        }
        widgets = {
            'preferred_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')


        # Валидация, что все необходимые поля заполнены
        if not address:
            raise ValidationError("Адрес не может быть пустым.")

        return cleaned_data


class AdminLoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=username, password=password)

        if user is None or not user.is_staff:
            raise forms.ValidationError("Неверный логин или пароль, или у вас нет прав администратора.")

        return cleaned_data
