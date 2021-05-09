from django import forms
from .models import Patient, Appointment, Clinic


class MyChoiceField(forms.ChoiceField):
    def valid_value(self, value):
        return True


class AppointmentForm(forms.Form):
    error_css_class = 'is-invalid'

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
            patient = Patient.objects.get(user=self.cleaned_data['user'],
                                          phone_number=self.cleaned_data['phone_number'])
        except Patient.DoesNotExist:
            patient, _ = Patient.objects.update_or_create(user=self.cleaned_data['user'],
                                                          defaults={'phone_number': self.cleaned_data['phone_number']})
        appointment = Appointment.objects.filter(
            clinic=clinic, date=self.cleaned_data['date'], time=self.cleaned_data['time']
        ).update(patient=patient, problem=self.cleaned_data['description'])
        return appointment
