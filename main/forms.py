from django import forms  # Импортируем модуль forms для создания форм
from django.contrib.auth import get_user_model, authenticate  # Импортируем функции для получения модели пользователя и аутентификации
from django.core.exceptions import ValidationError  # Импортируем класс для обработки ошибок валидации
from django.contrib.auth.password_validation import validate_password  # Импортируем функцию для проверки пароля

from main.models import Request  # Импортируем модель Request из приложения main


class UserLoginForm(forms.Form):  # Определяем форму для входа пользователя
    username = forms.CharField(label='Логин', max_length=150)  # Поле для ввода логина
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')  # Поле для ввода пароля с скрытым текстом

    def clean(self):  # Переопределяем метод clean для валидации данных формы
        cleaned_data = super().clean()  # Получаем очищенные данные из родительского метода
        username = cleaned_data.get('username')  # Получаем логин из очищенных данных
        password = cleaned_data.get('password')  # Получаем пароль из очищенных данных

        # Проверка на пустые поля
        if not username:  # Если логин пустой
            raise ValidationError("Логин не может быть пустым.")  # Выбрасываем ошибку валидации
        if not password:  # Если пароль пустой
            raise ValidationError("Пароль не может быть пустым.")  # Выбрасываем ошибку валидации

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=username, password=password)  # Аутентификация пользователя

        if user is None:  # Если пользователь не найден
            raise forms.ValidationError("Неверный логин или пароль.")  # Выбрасываем ошибку валидации

        return cleaned_data  # Возвращаем очищенные данные


class UserRegistrationForm(forms.ModelForm):  # Определяем форму для регистрации пользователя
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')  # Поле для ввода пароля
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')  # Поле для подтверждения пароля

    class Meta:  # Вложенный класс Meta для настройки формы
        model = get_user_model()  # Получаем модель пользователя
        fields = ['username', 'first_name', 'last_name', 'email']  # Определяем поля формы
        labels = {  # Задаем метки для полей формы
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }

    def clean(self):  # Переопределяем метод clean для валидации данных формы
        cleaned_data = super().clean()  # Получаем очищенные данные из родительского метода
        password = cleaned_data.get('password')  # Получаем пароль из очищенных данных
        confirm_password = cleaned_data.get('confirm_password')  # Получаем подтверждение пароля
        email = cleaned_data.get('email')  # Получаем email

        # Проверяем, что пароли совпадают
        if password and confirm_password and password != confirm_password:  # Если пароли не совпадают
            raise ValidationError("Пароли не совпадают.")  # Выбрасываем ошибку валидации

        # Проверка пароля
        try:
            validate_password(password)  # Проверяем, удовлетворяет ли пароль требованиям
        except ValidationError as e:  # Если возникают ошибки валидации
            raise ValidationError(f"Пароль не удовлетворяет требованиям: {e.messages}")  # Выбрасываем ошибку с сообщением

        # Валидация email (проверка уникальности и правильности формата)
        if email and get_user_model().objects.filter(email=email).exists():  # Если email уже зарегистрирован
            raise ValidationError("Этот адрес электронной почты уже зарегистрирован.")  # Выбрасываем ошибку валидации

        return cleaned_data  # Возвращаем очищенные данные

    def save(self, commit=True):  # Переопределяем метод save для сохранения пользователя
        user = super().save(commit=False)  # Создаем пользователя, не сохраняя его в базе данных
        user.set_password(self.cleaned_data['password'])  # Устанавливаем пароль (хэшируем его)
        if commit:  # Если нужно сохранить в базе данных
            user.save()  # Сохраняем пользователя
        return user  # Возвращаем созданного пользователя


class RequestForm(forms.ModelForm):  # Определяем форму для создания заявки
    class Meta:  # Вложенный класс Meta для настройки формы
        model = Request  # Указываем модель Request
        fields = ['address', 'service', 'preferred_date_time', 'payment_type']  # Определяем поля формы
        labels = {  # Задаем метки для полей формы
            'address': 'Адрес',
            'service': 'Услуга',
            'preferred_date_time': 'Дата и время',
            'payment_type': 'Тип оплаты',
        }
        widgets = {  # Настраиваем виджеты для полей формы
            'preferred_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Поле для выбора даты и времени
        }

    def clean(self):  # Переопределяем метод clean для валидации данных формы
        cleaned_data = super().clean()  # Получаем очищенные данные из родительского метода
        address = cleaned_data.get('address')  # Получаем адрес из очищенных данных

        # Валидация, что все необходимые поля заполнены
        if not address:  # Если адрес пустой
            raise ValidationError("Адрес не может быть пустым.")  # Выбрасываем ошибку валидации

        return cleaned_data  # Возвращаем очищенные данные


class AdminLoginForm(forms.Form):  # Определяем форму для входа администратора
    username = forms.CharField(label='Логин', max_length=150)  # Поле для ввода логина
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')  # Поле для ввода пароля с скрытым текстом

    def clean(self):  # Переопределяем метод clean для валидации данных формы
        cleaned_data = super().clean()  # Получаем очищенные данные из родительского метода
        username = cleaned_data.get('username')  # Получаем логин из очищенных данных
        password = cleaned_data.get('password')  # Получаем пароль из очищенных данных

        # Пытаемся аутентифицировать пользователя
        user = authenticate(username=username, password=password)  # Аутентификация пользователя

        if user is None or not user.is_staff:  # Если пользователь не найден или не является администратором
            raise forms.ValidationError("Неверный логин или пароль, или у вас нет прав администратора.")  # Выбрасываем ошибку валидации

        return cleaned_data  # Возвращаем очищенные данные
