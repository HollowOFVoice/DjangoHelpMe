from django.contrib import admin

from main.models import Request

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'address', 'preferred_date_time', 'payment_type', 'status', 'cancellation_reason')
    list_filter = ('status', 'payment_type', 'service')
    search_fields = ('user__username', 'address', 'service')

    # Поля, доступные для редактирования
    fields = ('user', 'service', 'address', 'preferred_date_time', 'payment_type', 'status', 'cancellation_reason')
    readonly_fields = ('user', 'service', 'address', 'preferred_date_time', 'payment_type')

    # Функция для изменения статуса с обязательным указанием причины отмены
    def save_model(self, request, obj, form, change):
        if obj.status == 'canceled' and not obj.cancellation_reason:
            raise ValueError("Причина отмены обязательна.")
        super().save_model(request, obj, form, change)

admin.site.register(Request, RequestAdmin)