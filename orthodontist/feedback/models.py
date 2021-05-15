from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from appointment.models import Appointment


def validate_appointment_date(value):
    appointment = Appointment.objects.get(id=value)

    if appointment.date > timezone.now().date():
        raise ValidationError(
            _('%(appointment)s от %(date)s еще не состоялся'),
            params={'appointment': appointment,'date': appointment.date},
        )

class Feedback(models.Model):
    comment = models.CharField(max_length=1000, verbose_name='Отзыв')
    name = models.CharField(max_length=40, verbose_name='Имя')
    email = models.EmailField(max_length=40, verbose_name='Электронная почта')
    appointment = models.ForeignKey(Appointment, null=True, default=None, blank=True, on_delete=models.SET_NULL,
                                       verbose_name='Прием', validators=[validate_appointment_date])
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отзыва')
    is_published = models.BooleanField(blank=True, default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'Отзыв № {self.id}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-date']
