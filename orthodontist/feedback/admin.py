from django.contrib import admin
from .models import Feedback


def publish_feedack(modeladmin, request, queryset):
    queryset.update(is_published=True)


def conceal_feedback(modeladmin, request, queryset):
    queryset.update(is_published=False)


publish_feedack.short_description = 'Опубликовать выбранные отзывы'
conceal_feedback.short_description = 'Скрыть выбранные отзывы'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'name', 'email', 'appointment_date', 'date')
    actions = [conceal_feedback, publish_feedack]

    def title(self, obj):
        return obj
    title.short_description = 'Отзыв'

    def appointment_date(self, obj):
        if obj.appointment:
            return obj.appointment.date
    appointment_date.short_description = 'Дата приема'


admin.site.register(Feedback, FeedbackAdmin)
