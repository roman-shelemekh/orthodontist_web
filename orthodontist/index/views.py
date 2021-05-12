from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count, Q
from django.utils import timezone
from ask.models import Question
from .forms import SignupForm, LoginForm, UserUpdateForm, ProfileUpdateForm, SearchForm


def index(request):
    return render(request, 'index/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            form.log_in(request, user)
            return HttpResponseRedirect(reverse('user', args=[request.user.id]))
    else:
        form = SignupForm()
    return render(request, 'index/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        url = request.POST.get('next', '/')
        if form.is_valid():
            if form.log_in(request):
                return HttpResponseRedirect(url)
            else:
                return render(request, 'index/login.html', {'form': form, 'error_message': 'Неверные логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'index/login.html', {'form': form})


class UserRatingMixin:

    def get_context_data(self, **kwargs):
        context = super(UserRatingMixin, self).get_context_data(**kwargs)
        rating = 0
        for question in self.object.question_set.all():
            rating += question.like.count()
        context['rating'] = rating
        return context


class UserView(UserRatingMixin, SingleObjectMixin, ListView):
    template_name = 'index/user.html'
    paginate_by = 5
    context_object_name = 'userdata'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Question.objects.annotated()
        return queryset.order_by('-date')


class UserViewPopular(UserView):
    template_name = 'index/user_popular.html'

    def get_queryset(self):
        queryset = super(UserViewPopular, self).get_queryset()
        return queryset.order_by('-like_count')


class UserViewUpdate(UserRatingMixin, DetailView):
    model = User
    template_name = 'index/user_update.html'
    context_object_name = 'userdata'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.id:
            return HttpResponseForbidden()
        self.u_form = UserUpdateForm(instance=request.user)
        self.p_form = ProfileUpdateForm(instance=request.user.profile)
        return super(UserViewUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserViewUpdate, self).get_context_data(**kwargs)
        context['u_form'] = self.u_form
        context['p_form'] = self.p_form
        return context

    def post(self, request, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        emails = User.objects.exclude(id=request.user.id).values_list('email', flat=True)
        if u_form.is_valid() and p_form.is_valid() and u_form.cleaned_data['email'] not in emails:
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профель изменен')
            return HttpResponseRedirect(reverse('user', args=(request.user.id,)))
        else:
            if u_form.cleaned_data['email'] in emails:
                u_form.add_error(field='email', error='Пользователь с таким электронным адресом уже существует.')
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            context['u_form'] = u_form
            context['p_form'] = p_form
            return render(request, 'index/user_update.html', context)


class UserViewAppointments(UserRatingMixin, DetailView):
    model = User
    template_name = 'index/user_appointments.html'
    context_object_name = 'userdata'

    def dispatch(self, request, *args, **kwargs):
        if kwargs['pk'] != request.user.id:
            return HttpResponseForbidden()
        return super(UserViewAppointments, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserViewAppointments, self).get_context_data(**kwargs)
        context['future_appointments'] = context['userdata']\
            .patient.appointment_set.filter(date__gte=timezone.now().date()).order_by('date')
        context['past_appointments'] = context['userdata']\
            .patient.appointment_set.filter(date__lt=timezone.now().date()).order_by('-date')
        return context



class SearchResults(ListView):
    model = Question
    template_name = 'index/search.html'
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        self.form = SearchForm(request.GET)
        self.form.is_valid()
        return super(SearchResults, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Question.objects.all()
        queryset = queryset.annotate(answers_count=Count('answer__id'))
        queryset = queryset.annotate(like_count=Count('like__id'))
        if not self.form.cleaned_data.get('search_by') or self.form.cleaned_data.get('search_by') == "default":
            queryset = queryset.filter(Q(text__icontains=self.form.cleaned_data.get('search_input')) |
                                       Q(title__icontains=self.form.cleaned_data.get('search_input')))
        elif self.form.cleaned_data.get('search_by') == "question_title":
            queryset = queryset.filter(title__icontains=self.form.cleaned_data.get('search_input'))
        elif self.form.cleaned_data.get('search_by') == "question_text":
            queryset = queryset.filter(text__icontains=self.form.cleaned_data.get('search_input'))
        elif self.form.cleaned_data.get('search_by') == "question_author":
            filter = '|'.join(self.form.cleaned_data.get('search_input').split())
            queryset = queryset.filter(Q(author__first_name__iregex=filter) | Q(author__last_name__iregex=filter))
        if not self.form.cleaned_data.get('order_by') or self.form.cleaned_data.get('order_by') == "new":
            queryset = queryset.order_by('-date')
        elif self.form.cleaned_data.get('order_by') == "old":
            queryset = queryset.order_by('date')
        elif self.form.cleaned_data.get('order_by') == "popular":
            queryset = queryset.order_by('-like_count')
        elif self.form.cleaned_data.get('order_by') == "answers":
            queryset = queryset.order_by('-answers_count')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchResults, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
