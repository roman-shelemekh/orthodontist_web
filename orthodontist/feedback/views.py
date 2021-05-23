from django.shortcuts import reverse
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from appointment.models import Appointment


class FeedbackView(FormMixin, ListView):
    template_name = 'feedback/feedback.html'
    context_object_name = 'feedbacks'
    form_class = FeedbackForm
    paginate_by = 10

    def get_success_url(self):
        return reverse('feedback:index')

    def get_form_kwargs(self):
        kwargs = super(FeedbackView, self).get_form_kwargs()
        if self.request.method == 'POST' and self.request.user.is_authenticated:
            print(kwargs)
            kwargs['data']._mutable = True
            kwargs['data']['name'] = self.request.user.first_name
            kwargs['data']['email'] = self.request.user.email
            if kwargs['data']['appointment']:
                kwargs['data']['appointment'] = Appointment.objects.get(id=kwargs['data']['appointment'])
            kwargs['data']._mutable = False
            print(kwargs)
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Ваш отзыв будет опубликован в ближайшее время')
        return super(FeedbackView, self).form_valid(form)

    def form_invalid(self, form):
        form.validation_error_class()
        return super(FeedbackView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_queryset(self):
        return Feedback.objects.filter(is_published=True)
