from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, RequestForm, UserLoginForm, AdminLoginForm
from .models import Request

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Убедитесь, что передаете request

            if user is not None:
                login(request, user)  # Авторизация пользователя
                return redirect('home')  # Перенаправление на главную страницу после успешного входа
            else:
                form.add_error(None, "Неверный логин или пароль.")  # Добавляем ошибку, если не удалось аутентифицировать пользователя
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем пользователя, но не сохраняем его сразу
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()  # Сохраняем пользователя в базе данных
            return redirect('login')  # Перенаправляем на страницу входа
    else:
        form = UserRegistrationForm()

    return render(request, 'registration.html', {'form': form})


@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user  # Связываем запрос с текущим пользователем
            new_request.save()
            return redirect('home')  # Перенаправляем на страницу с успешной подачей запроса
    else:
        form = RequestForm()

    return render(request, 'create_request.html', {'form': form})


def main(request):
    return render(request, 'main.html')

def home(request):
    return render(request, 'home.html')


@login_required
def request_history(request):
    # Получаем все заявки текущего пользователя
    requests = Request.objects.filter(user=request.user).order_by('-preferred_date_time')

    # Передаем их в шаблон
    return render(request, 'request_history.html', {'requests': requests})



def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_request_history')  # Перенаправление на страницу просмотра заявок
            else:
                form.add_error(None, "Неверный логин или пароль, или у вас нет прав администратора.")
    else:
        form = AdminLoginForm()

    return render(request, 'admin_login.html', {'form': form})



@login_required
def admin_request_history(request):
    if not request.user.is_staff:  # Проверка прав администратора
        return redirect('home')  # Перенаправляем на главную страницу, если не администратор

    requests = Request.objects.all()  # Получаем все заявки

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('new_status')
        cancellation_reason = request.POST.get('cancellation_reason')

        # Обработка изменения статуса заявки
        try:
            req = Request.objects.get(id=request_id)
            if new_status == 'canceled' and not cancellation_reason:
                raise ValueError("Причина отмены обязательна.")
            req.status = new_status
            req.cancellation_reason = cancellation_reason if new_status == 'canceled' else None
            req.save()
        except Request.DoesNotExist:
            pass  # Заявка не найдена

        return redirect('admin_request_history')  # Перенаправляем на страницу с заявками

    return render(request, 'admin_request_history.html', {'requests': requests})


def admin_requests(request):
    requests = Request.objects.all()
    return render(request, 'admin_requests.html', {'requests': requests})