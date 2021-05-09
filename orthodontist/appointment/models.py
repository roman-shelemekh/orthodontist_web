from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# class ClinicManager(models.Manager):
#     def select_options(self):
#         options = list()
#         names = self.values_list('name', flat=True)
#         for name in names:
#             options.append((name, name))
#         return options


class Clinic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название клиника', unique=True)
    address = models.CharField(max_length=100, verbose_name='Адрес клиники', unique=True)
    # objects = ClinicManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клинику'
        verbose_name_plural = 'Клиники'


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пациент')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', unique=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'пациента'
        verbose_name_plural = 'Пациенты'

class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name='Название клиника')
    date = models.DateField(verbose_name='Дата приема')
    time = models.TimeField(verbose_name='Время приема')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default=None, blank=True,
                                verbose_name='Пациент')
    problem = models.TextField(max_length=1000, verbose_name='Описание проблемы', null=True, default=None, blank=True)

    def __str__(self):
        return f'Запись № {self.id}'

    def is_available(self):
        if self.date > timezone.now().date() and not self.patient:
            return '- свободно -'
        elif self.patient:
            return '- запись -'
        else:
            return '- просрочено -'
    is_available.short_description = 'Статус'

    class Meta:
        unique_together = ('date', 'time')
        verbose_name = 'запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-date', '-time', 'clinic']
