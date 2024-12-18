from django.template.context_processors import request
from django.urls import path

from main.views import register, create_request, user_login, main, home, request_history,admin_request_history,admin_login

# Определяем маршруты URL для приложения
urlpatterns = [
    path('register/', register, name='register'),  # URL для регистрации пользователя
    path('', main, name='main'),                   # URL для главной страницы
    path('home/', home, name='home'),              # URL для домашней страницы
    path('login/', user_login, name='login'),      # URL для входа пользователя
    path('request/', create_request, name='request'),  # URL для создания новой заявки
    path('request_history/', request_history, name='request_history'),  # URL для истории заявок пользователя
    path('admin_login/', admin_login, name='admin_login'),  # URL для входа администратора
    path('admin_request_history/', admin_request_history, name='admin_request_history'),  # URL для истории заявок администратора
]
