from django.db import models
from django.utils import timezone


class Clinic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название клиника', unique=True)
    address = models.CharField(max_length=100, verbose_name='Адрес клиники', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клинику'
        verbose_name_plural = 'Клиники'


class Patient(models.Model):
    name = models.CharField(max_length=40, verbose_name='Имя')
    email = models.EmailField(max_length=40, verbose_name='Электронная почта', unique=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пациента'
        verbose_name_plural = 'Пациенты'

class Appointment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, verbose_name='Название клиника')
    date = models.DateField(verbose_name='Дата приема')
    time = models.TimeField(verbose_name='Время приема')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, default=None, blank=True,
                                verbose_name='Пациент')
    problem = models.TextField(max_length=1000, verbose_name='Описание проблемы', null=True, default=None, blank=True)

    def __str__(self):
        return f'Прием № {self.id}'

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
        verbose_name_plural = 'записи на прием'
        ordering = ['-date', '-time', 'clinic']
