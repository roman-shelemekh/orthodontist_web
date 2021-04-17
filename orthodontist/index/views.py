from django.shortcuts import render, HttpResponseRedirect, reverse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Count, Q
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


# class UserView(DetailView):
#     model = User
#     template_name = 'index/user.html'
#     context_object_name = 'userdata'
#
#
#     def get_context_data(self, **kwargs):
#         context = super(UserView, self).get_context_data()
#         userd = kwargs['object']
#         user_questions = Question.objects.filter(author=userd).order_by('-date')[:5]
#         user_questions = user_questions.annotate(answers_count=Count('answer__id'))
#         context['user_questions'] = user_questions
#         rating = 0
#         for question in userd.question_set.all():
#             rating += question.like.count()
#         context['rating'] = rating
#         return context

class UserView(SingleObjectMixin, ListView):
    template_name = 'index/user.html'
    paginate_by = 5
    context_object_name = 'userdata'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        print(self.object)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating = 0
        for question in self.object.question_set.all():
            rating += question.like.count()
        context['rating'] = rating
        return context

    def get_queryset(self):
        queryset = self.object.question_set.all()
        queryset = queryset.order_by('-date')
        queryset = queryset.annotate(answers_count=Count('answer__id'))
        return queryset


# class UserViewPopular(DetailView):
#     model = User
#     template_name = 'index/user_popular.html'
#     context_object_name = 'userdata'
#
#     def get_context_data(self, **kwargs):
#         context = super(UserViewPopular, self).get_context_data()
#         userd = kwargs['object']
#         user_questions = Question.objects.filter(author=userd)
#         user_questions = user_questions.annotate(like_count=Count('like__id'))
#         user_questions = user_questions.order_by('-like_count')[:5]
#         user_questions = user_questions.annotate(answers_count=Count('answer__id'))
#         context['user_questions'] = user_questions
#         rating = 0
#         for question in userd.question_set.all():
#             rating += question.like.count()
#         context['rating'] = rating
#         return context


class UserViewPopular(UserView):

    def get_queryset(self):
        queryset = self.object.question_set.all()
        queryset = queryset.annotate(like_count=Count('like__id'))
        queryset = queryset.order_by('-like_count')
        queryset = queryset.annotate(answers_count=Count('answer__id'))
        return queryset



# @method_decorator(login_required, name='dispatch')
# class UserViewUpdate(DetailView):
#     model = User
#     template_name = 'index/user_update.html'
#     context_object_name = 'userdata'
#
#
#     def get_context_data(self, **kwargs):
#         context = super(UserViewUpdate, self).get_context_data()
#         object = kwargs['object']
#         rating = 0
#         for question in object.question_set.all():
#             rating += question.like.count()
#         context['rating'] = rating
#         u_form = UserUpdateForm(instance=object)
#         p_form = ProfileUpdateForm(instance=object.profile)
#         context['u_form'] = u_form
#         context['p_form'] = p_form
#         return context

class UserViewUpdate(DetailView):
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
        rating = 0
        for question in self.object.question_set.all():
            rating += question.like.count()
        context['rating'] = rating
        context['u_form'] = self.u_form
        context['p_form'] = self.p_form
        return context

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Ваш профель изменен')
            return HttpResponseRedirect(reverse('user', args=(request.user.id,)))
        else:
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            context['u_form'] = u_form
            context['p_form'] = p_form
            return render(request, 'index/user_update.html', context)



# @login_required
# def user_update_post(request, pk):
#     print('hello')
#     if request.method == 'POST':
#         print('hello2')
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             print('hello3')
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'Ваш профель изменен')
#             return HttpResponseRedirect(reverse('user', args=(request.user.id,)))
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)
#     context = {'u_form': u_form, 'p_form': p_form}
#     return render(request, 'index/user_update.html', context)


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
            queryset = queryset.filter(Q(text__icontains=self.form.cleaned_data.get('search_input')
                                                 ) | Q(title__icontains=self.form.cleaned_data.get('search_input')))
        elif self.form.cleaned_data.get('search_by') == "question_title":
            queryset = queryset.filter(title__icontains=self.form.cleaned_data.get('search_input'))
        elif self.form.cleaned_data.get('search_by') == "question_text":
            queryset = queryset.filter(text__icontains=self.form.cleaned_data.get('search_input'))
        elif self.form.cleaned_data.get('search_by') == "question_author":
            queryset = queryset.filter(author__username=self.form.cleaned_data.get('search_input'))
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