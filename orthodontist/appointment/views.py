from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils import timezone
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Clinic, Appointment


class AppointmentView(FormView):
    template_name = 'appointment/appointment.html'
    form_class = AppointmentForm
    success_url = '/'

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        form.save()
        return super(AppointmentView, self).form_valid(form)

    def form_invalid(self, form):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        return super(AppointmentView, self).form_invalid(form)
    
    
def get_clinics(request):
    if request.is_ajax():
        clinics = Clinic.objects.filter(appointment__patient=None,
                                        appointment__date__gt=timezone.now().date()).order_by('name')
        data = {'clinics': list(clinics.values_list('name', flat=True).distinct())}
        return JsonResponse(data, status=200)

def get_dates(request):
    if request.is_ajax():
        clinic = request.GET.get('clinic')
        appointments = Appointment.objects.filter(clinic__name=clinic,
                                                  date__gt=timezone.now().date(),
                                                  patient=None).order_by('date')
        data = {'dates': list(set(appointments.values_list('date', flat=True)))}
        return JsonResponse(data, status=200)

def get_timetable(request):
    if request.is_ajax():
        clinic = request.GET.get('clinic')
        date = request.GET.get('date')
        appointments = Appointment.objects.filter(clinic__name=clinic,
                                                  date=date,
                                                  patient=None).order_by('time')
        data = {'timetable': list(appointments.values_list('time', flat=True))}
        return JsonResponse(data, status=200)