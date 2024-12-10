from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В работе'),
        ('completed', 'Услуга оказана'),
        ('canceled', 'Услуга отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100)
    service_name = models.CharField(max_length=100)  # Поле для названия услуги
    service_description = models.TextField(blank=True, null=True)  # Описание услуги (по желанию)
    date = models.DateField()
    time = models.TimeField()
    payment_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.user.username} - {self.service_name}"

    # Модель для простых пользователей
class SimpleUser (models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)  # Убедитесь, что поле существует
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)  # Храните хэш пароля

    def __str__(self):
        return self.username