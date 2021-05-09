from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.utils import timezone
from django.db import models
from .models import Clinic, Appointment, Patient
import datetime
from django.utils.translation import gettext_lazy as _


class MyDateFilter(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super(MyDateFilter, self).__init__(field, request, params, model, model_admin, field_path)
        now = timezone.now()
        if timezone.is_aware(now):
            now = timezone.localtime(now)
        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.links = (
            (_('Любая дата'), {}),
            (('Сегодня'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(tomorrow),
            }),
            (_('Следующие 7 дней'), {
                self.lookup_kwarg_since: str(today),
                self.lookup_kwarg_until: str(today + datetime.timedelta(days=7)),
            }),
            (_('Этот месяц'), {
                self.lookup_kwarg_since: str(today.replace(day=1)),
                self.lookup_kwarg_until: str(next_month),
            }),
            (_('Этот год'), {
                self.lookup_kwarg_since: str(today.replace(month=1, day=1)),
                self.lookup_kwarg_until: str(next_year),
            }),
        )


class AvailabilityFilter(admin.SimpleListFilter):
    title = _('Статус')
    parameter_name = 'availability'

    def lookups(self, request, model_admin):
        return (
            ('available', _('Предстоящие приемы, доступные для записи')),
            ('occupied', _('Предстоящие приемы с записью')),
            ('overdue', _('Прошедшие приемы')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(date__gt=timezone.now().date(), patient=None)
        if self.value() == 'overdue':
            return queryset.filter(date__lte=timezone.now().date())
        if self.value() == 'occupied':
            return queryset.filter(date__gte=timezone.now().date()).exclude(patient=None)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_available', 'clinic', 'date', 'time', 'patient')
    list_filter = [AvailabilityFilter, 'clinic', ('date', MyDateFilter)]

    def title(self, obj):
        # self.if_empty(obj)
        return obj
    title.short_description = 'Запись'

    # def if_empty(self, obj):
    #     if not obj.patient and obj.date > timezone.now().date():
    #         self.empty_value_display = '- свободно -'
    #     else:
    #         self.empty_value_display = '- просрочено -'


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone_number', 'email')

    def patient_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    patient_name.short_description = 'Пациент'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Электронный адрес'


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(Patient, PatientAdmin)

