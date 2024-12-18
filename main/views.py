from django.contrib.auth import authenticate, login  # Импортируем функции для аутентификации и входа пользователя
from django.contrib.auth.decorators import login_required  # Импортируем декоратор для проверки аутентификации
from django.shortcuts import render, redirect  # Импортируем функции для рендеринга шаблонов и перенаправления
from .forms import UserRegistrationForm, RequestForm, UserLoginForm, AdminLoginForm  # Импортируем формы
from .models import Request  # Импортируем модель Request

def user_login(request):  # Функция для обработки входа пользователя
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        form = UserLoginForm(request.POST)  # Создаем экземпляр формы с данными из запроса
        if form.is_valid():  # Проверяем, валидна ли форма
            username = form.cleaned_data['username']  # Получаем логин из очищенных данных формы
            password = form.cleaned_data['password']  # Получаем пароль из очищенных данных формы
            user = authenticate(request, username=username, password=password)  # Аутентификация пользователя

            if user is not None:  # Если аутентификация прошла успешно
                login(request, user)  # Авторизуем пользователя
                return redirect('home')  # Перенаправляем на главную страницу после успешного входа
            else:
                form.add_error(None, "Неверный логин или пароль.")  # Добавляем ошибку, если не удалось аутентифицировать пользователя
    else:
        form = UserLoginForm()  # Создаем пустую форму для входа

    return render(request, 'login.html', {'form': form})  # Рендерим шаблон входа с формой


def register(request):  # Функция для регистрации нового пользователя
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        form = UserRegistrationForm(request.POST)  # Создаем экземпляр формы с данными из запроса
        if form.is_valid():  # Проверяем, валидна ли форма+
            user = form.save(commit=False)  # Создаем пользователя, но не сохраняем его сразу
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()  # Сохраняем пользователя в базе данных
            return redirect('login')  # Перенаправляем на страницу входа после успешной регистрации
    else:
        form = UserRegistrationForm()  # Создаем пустую форму для регистрации

    return render(request, 'registration.html', {'form': form})  # Рендерим шаблон регистрации с формой


@login_required  # Декоратор, который требует аутентификации для доступа к функции
def create_request(request):  # Функция для создания новой заявки
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        form = RequestForm(request.POST)  # Создаем экземпляр формы с данными из запроса
        if form.is_valid():  # Проверяем, валидна ли форма
            new_request = form.save(commit=False)  # Создаем заявку, но не сохраняем ее сразу
            new_request.user = request.user  # Связываем заявку с текущим пользователем
            new_request.save()  # Сохраняем заявку в базе данных
            return redirect('home')  # Перенаправляем на главную страницу после успешной подачи заявки
    else:
        form = RequestForm()  # Создаем пустую форму для заявки

    return render(request, 'create_request.html', {'form': form})  # Рендерим шаблон создания заявки с формой


def main(request):  # Функция для отображения главной страницы
    return render(request, 'main.html')  # Рендерим шаблон главной страницы


def home(request):  # Функция для отображения домашней страницы
    return render(request, 'home.html')  # Рендерим шаблон домашней страницы


@login_required  # Декоратор, который требует аутентификации для доступа к функции
def request_history(request):  # Функция для отображения истории заявок текущего пользователя
    requests = Request.objects.filter(user=request.user).order_by('-preferred_date_time')  # Получаем все заявки текущего пользователя, отсортированные по дате

    return render(request, 'request_history.html', {'requests': requests})  # Рендерим шаблон истории заявок с данными


def admin_login(request):  # Функция для обработки входа администратора
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        form = AdminLoginForm(request.POST)  # Создаем экземпляр формы с данными из запроса
        if form.is_valid():  # Проверяем, валидна ли форма
            username = form.cleaned_data['username']  # Получаем логин из очищенных данных формы
            password = form.cleaned_data['password']  # Получаем пароль из очищенных данных формы
            user = authenticate(request, username=username, password=password)  # Аутентификация пользователя

            if user is not None and user.is_staff:  # Если аутентификация прошла успешно и пользователь является администратором
                login(request, user)  # Авторизуем администратора
                return redirect('admin_request_history')  # Перенаправляем на страницу просмотра заявок администратора
            else:
                form.add_error(None, "Неверный логин или пароль, или у вас нет прав администратора.")  # Добавляем ошибку, если не удалось аутентифицировать администратора
    else:
        form = AdminLoginForm()  # Создаем пустую форму для входа администратора

    return render(request, 'admin_login.html', {'form': form})  # Рендерим шаблон входа администратора с формой


@login_required  # Декоратор, который требует аутентификации для доступа к функции
def admin_request_history(request):  # Функция для отображения истории заявок для администратора
    if not request.user.is_staff:  # Проверка, является ли пользователь администратором
        return redirect('home')  # Перенаправляем на главную страницу, если не администратор

    requests = Request.objects.all()  # Получаем все заявки

    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        request_id = request.POST.get('request_id')  # Получаем ID заявки из POST-запроса
        new_status = request.POST.get('new_status')  # Получаем новый статус заявки
        cancellation_reason = request.POST.get('cancellation_reason')  # Получаем причину отмены заявки

        # Обработка изменения статуса заявки
        try:
            req = Request.objects.get(id=request_id)  # Получаем заявку по ID
            if new_status == 'canceled' and not cancellation_reason:  # Проверка, если статус отменен, но причина не указана
                raise ValueError("Причина отмены обязательна.")  # Выбрасываем ошибку, если причина отмены не указана
            req.status = new_status  # Устанавливаем новый статус заявки
            req.cancellation_reason = cancellation_reason if new_status == 'canceled' else None  # Устанавливаем причину отмены, если статус отменен
            req.save()  # Сохраняем изменения в базе данных
        except Request.DoesNotExist:  # Если заявка не найдена
            pass  # Игнорируем ошибку (можно добавить логирование)

        return redirect('admin_request_history')  # Перенаправляем на страницу с заявками администратора

    return render(request, 'admin_request_history.html', {'requests': requests})  # Рендерим шаблон истории заявок администратора с данными


def admin_requests(request):  # Функция для отображения всех заявок администратора
    requests = Request.objects.all()  # Получаем все заявки
    return render(request, 'admin_requests.html', {'requests': requests})  # Рендерим шаблон с заявками
