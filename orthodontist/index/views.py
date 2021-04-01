from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignupForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.db.models import Count
from ask.models import Question


def index(request):
    return render(request, 'index/index.html')


def signup(request):
    if request.method == 'POST':
        print('1')
        form = SignupForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print('2')
            user = form.save()
            form.log_in(request,user)
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


class UserView(generic.DetailView):
    model = User
    template_name = 'index/user.html'
    context_object_name = 'userdata'


    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data()
        user_questions = Question.objects.filter(author=kwargs['object']).order_by('-date')
        user_questions = user_questions.annotate(answers_count=Count('answer__id'))
        context['user_questions'] = user_questions
        return context


@login_required
def user_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профель изменен')
            return HttpResponseRedirect(reverse('user', args=(request.user.id,)))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'index/user_update.html', context)