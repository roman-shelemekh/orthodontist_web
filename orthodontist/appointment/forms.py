from django import forms
from django.core.mail import send_mail
from .models import Patient, Appointment, Clinic
import re
from datetime import datetime


class MyChoiceField(forms.ChoiceField):
    def valid_value(self, value):
        return True


class AppointmentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
                           label='Имя')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                            label='Email')
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
                                   label='Номер телефона')
    clinic = MyChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Клиника')
    date = MyChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Дата')
    time = MyChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Время')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', ' style': 'height: 100px', 'placeholder': 'Описание'}),
                                  label='Краткое изложение проблемы')

    def save(self):
        clinic = Clinic.objects.get(name=self.cleaned_data['clinic'])
        try:
            patient = Patient.objects.get(name=self.cleaned_data['name'],
                                          email=self.cleaned_data['email'],
                                          phone_number=self.cleaned_data['phone_number'])
        except Patient.DoesNotExist:
            patient, _ = Patient.objects.update_or_create(email=self.cleaned_data['email'],
                                                          defaults={'phone_number': self.cleaned_data['phone_number'],
                                                                    'name': self.cleaned_data['name']})
        appointment = Appointment.objects.filter(
            clinic=clinic, date=self.cleaned_data['date'], time=self.cleaned_data['time']
        ).update(patient=patient, problem=self.cleaned_data['description'])
        return appointment

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not re.match(r'^\+[\d]{11}$', phone_number):
            raise forms.ValidationError('Телефон должен быть записан в формате +7XXXXXXXXXX.')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^\S+@\S+\.\S+$', email):
            raise forms.ValidationError('Введите корректный электронный адрес.')
        return email

    def send_email(self):
        date = datetime.strptime(self.cleaned_data['date'], '%Y-%m-%d')
        time = datetime.strptime(self.cleaned_data['time'], '%H:%M:%S')
        recipients = ['orthodental@tut.by', self.cleaned_data['email']]
        subject = 'Запись на прием к врачу-ортодонту'
        message = 'Уважаемый(-ая) ' + self.cleaned_data['name'] + \
                  ', \n\nВы успешно записались на прием к врачу-ортодонту Екатерине Бахур, который состоится ' + \
                 date.strftime('%d.%m.%Y') + ' в ' + time.strftime('%H:%M') + \
                  '. C Вами свяжутся заранее, чтобы уточнить делали визита. \n\nБлагодарим за интерес к нашим услугам!'
        sender = 'orthodental@tut.by'
        send_mail(subject, message, sender, recipients)