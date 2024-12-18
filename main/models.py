from django.contrib.auth.models import User  # Импортируем модель User для связи с пользователями
from django.db import models  # Импортируем модуль models для создания моделей базы данных


class Request(models.Model):  # Определяем модель Request, которая будет представлять заявку
    # Определяем возможные статусы заявки
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),  # Новый статус
        ('in_progress', 'В работе'),  # Статус "В работе"
        ('completed', 'Услуга оказана'),  # Статус "Услуга оказана"
        ('canceled', 'Услуга отменена'),  # Статус "Услуга отменена"
    ]

    # Определяем возможные способы оплаты
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),  # Оплата наличными
        ('card', 'Банковская карта'),  # Оплата банковской картой
    ]

    # Определяем доступные виды услуг
    SERVICE_CHOICES = [
        ('general_cleaning', 'Общий клининг'),  # Общий клининг
        ('deep_cleaning', 'Генеральная уборка'),  # Генеральная уборка
        ('post_construction_cleaning', 'Послестроительная уборка'),  # Послестроительная уборка
        ('dry_cleaning', 'Химчистка'),  # Химчистка
    ]

    # Связь с моделью User (пользователь), если пользователь удален, все его заявки также будут удалены
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    # Поле для хранения адреса, где будет оказана услуга
    address = models.CharField(max_length=255, verbose_name='Адрес')

    # Поле для выбора услуги из заранее определенного списка
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name='Услуга')

    # Поле для указания предпочтительной даты и времени оказания услуги
    preferred_date_time = models.DateTimeField(null=True, verbose_name='Дата и время')

    # Поле для выбора типа оплаты из заранее определенного списка
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name='Тип оплаты')

    # Поле для хранения статуса заявки с значением по умолчанию 'new'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    # Поле для указания причины отмены заявки, если таковая имеется
    cancellation_reason = models.TextField(blank=True, null=True, verbose_name='Причина отмены')

    # Метод для отображения информации о заявке в виде строки
    def __str__(self):
        return f"{self.user.username} - {self.service}"

    # Метод для изменения статуса заявки
    def change_status(self, new_status):
        # Проверка, является ли новый статус допустимым
        if new_status not in dict(self.STATUS_CHOICES).keys():
            raise ValueError("Недопустимый статус.")  # Если статус недопустимый, выбрасываем исключение
        self.status = new_status  # Обновляем статус заявки
        self.save()  # Сохраняем изменения в базе данных