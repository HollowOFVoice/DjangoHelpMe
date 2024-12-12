from django.template.context_processors import request
from django.urls import path

from main.views import register, create_request, user_login, main, home, request_history,admin_request_history,admin_login

urlpatterns = [
    path('register/', register, name='register'),
    path('', main, name='main'),
    path('home/', home, name='home'),  # Главная страница
    path('login/', user_login, name='login'),
    path('request/', create_request, name='request'),
path('request_history/', request_history, name='request_history'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_request_history/', admin_request_history, name='admin_request_history'),
]
