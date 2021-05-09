from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from django.http import JsonResponse
from .forms import AppointmentForm
from .models import Clinic, Appointment


class AppointmentView(TemplateView):
    template_name = 'appointment/appointment.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = AppointmentForm()
        return super(AppointmentView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AppointmentView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
    
    
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