from django import forms
from .models import Clinic
from django.urls import reverse


class AppointmentForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
                                   label='Номер телефона')
    clinic = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Клиника')
    date = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Дата')
    time = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label='Время')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', ' style': 'height: 100px', 'placeholder': 'Описание'}),
                                  label='Краткое изложение проблемы')