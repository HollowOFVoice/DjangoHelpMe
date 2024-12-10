from django.template.context_processors import request
from django.urls import path

from main.views import registration, main, login_view, create_request

urlpatterns = [
    path('register/', registration, name='register'),
    path('', main, name='main'),
    path('login/', login_view, name='login'),
    path('request/', create_request, name='request'),
]
