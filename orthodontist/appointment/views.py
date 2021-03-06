from django.shortcuts import reverse, get_object_or_404
from django.views.generic.edit import FormView
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponseRedirect
from .forms import AppointmentForm
from .models import Clinic, Appointment
from .serializers import ClinicSerializer
from .tasks import send_email
from rest_framework.generics import ListAPIView


class AppointmentView(FormView):
    template_name = 'appointment/appointment.html'
    form_class = AppointmentForm

    def get_form_kwargs(self):
        kwargs = super(AppointmentView, self).get_form_kwargs()
        if self.request.method == 'POST' and self.request.user.is_authenticated:
            kwargs['data']._mutable = True
            kwargs['data']['name'] = self.request.user.first_name
            kwargs['data']['email'] = self.request.user.email
            kwargs['data']._mutable = False
        return kwargs

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('appointments', args=[self.request.user.id])
        else:
            return reverse('appointment:index')

    def form_valid(self, form):
        form.save()
        send_email.delay(form.cleaned_data['date'], form.cleaned_data['time'],
                         form.cleaned_data['name'], form.cleaned_data['email'])
        messages.success(self.request, 'Вы успешно записались на прием. '
                                       'Сообщение с информацией о приеме отправлено на вашу почту')
        return super(AppointmentView, self).form_valid(form)

    def form_invalid(self, form):
        form.validation_error_class()
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
                                                  patient=None).order_by('date').distinct('date')
        data = {'dates': list(appointments.values_list('date', flat=True))}
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

def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.user.email == appointment.patient.email:
        appointment.patient = None
        appointment.problem = None
        appointment.save()
        messages.success(request, 'Вы успешно отменили запись на прием.')
        return HttpResponseRedirect(reverse('appointments', args=[request.user.id]))
    else:
        raise Http404()


class ClinicsForMap(ListAPIView):
    queryset = Clinic.objects.all().order_by('name')
    serializer_class = ClinicSerializer
    pagination_class = None

    def initial(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()
        return super(ClinicsForMap, self).initial(request, *args, **kwargs)