from django.contrib.auth.hashers import make_password

from main.forms import UserRegistrationForm, RequestForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import SimpleUser
from django.contrib.auth.hashers import check_password

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем в БД сразу
            user.password = make_password(form.cleaned_data['password'])  # Хэшируем пароль
            user.save()  # Сохраняем пользователя
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = SimpleUser.objects.get(username=username)
            if check_password(password, user.password):
                # Успешный вход, вы можете установить сессию или перенаправить на другую страницу
                return redirect('home')  # Перенаправление на главную страницу
            else:
                return render(request, 'login.html', {'error': 'Неверные данные'})
        except SimpleUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'Неверные данные'})
    return render(request, 'login.html')

def main(request):
    return render(request, 'main.html')

def profile_view(request):
    # Получаем текущего пользователя
    username = request.user.first_name  # Или request.user.username, если хотите использовать имя пользователя
    return render(request, 'home.html', {'username': username})

def home(request):
    return render(request, 'home.html')



def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)  # Не сохраняем сразу в БД
            request_obj.user = request.user  # Привязываем заявку к текущему пользователю
            request_obj.save()  # Сохраняем заявку в БД
            return redirect('home')  # Перенаправляем на страницу успеха или другую страницу
    else:
        form = RequestForm()

    return render(request, 'create_request.html', {'form': form})