from django.contrib.auth.models import User
from django.db import models


class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В работе'),
        ('completed', 'Услуга оказана'),
        ('canceled', 'Услуга отменена'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]

    SERVICE_CHOICES = [
        ('general_cleaning', 'Общий клининг'),
        ('deep_cleaning', 'Генеральная уборка'),
        ('post_construction_cleaning', 'Послестроительная уборка'),
        ('dry_cleaning', 'Химчистка'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name='Услуга',)  # Добавьте значение по умолчанию
    preferred_date_time = models.DateTimeField(null=True, verbose_name='Дата и время')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name='Тип оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name='Причина отмены')

    def __str__(self):
        return f"{self.user.username} - {self.service}"

    def change_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES).keys():
            raise ValueError("Недопустимый статус.")
        self.status = new_status
        self.save()