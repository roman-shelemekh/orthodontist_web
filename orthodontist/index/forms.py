from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email',
                                                                'placeholder':'Электронный адрес'}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), label='Запомнить меня',
                                         required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].help_text = '* Ваш пароль должен содержать как минимум 8 символов и не может состоять только из цифр'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

    def log_in(self, request, user):
        login(request, user)
        if self.cleaned_data['remember_me']:
            request.session.set_expiry(timedelta(days=30).total_seconds())
        else:
            request.session.set_expiry(0)


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                             'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type':'checkbox'}), label='Запомнить меня',
                                     required=False)

    def log_in(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        remember_me = self.cleaned_data['remember_me']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if remember_me:
                request.session.set_expiry(timedelta(days=30).total_seconds())
            else:
                request.session.set_expiry(0)
            return True

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email',
                                                                'placeholder':'Электронный адрес'}))

    class Meta:
        model = User
        fields = ['username', 'email']


    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        labels = {
            "image": "Фото профиля"
        }

SEARCH_OPTIONS = [
    ('default', 'заголовку и содержанию'),
    ('question_title', 'заголовку'),
    ('question_text', 'содержанию'),
    ('question_author', 'автору'),
]

ORDER_BY = [
    ('new', 'дате - сначала новые'),
    ('old', 'дате - сначала старые'),
    ('popular', 'популярности'),
    ('answers', 'обсуждаемости')
]

class SearchForm(forms.Form):
    search_input = forms.CharField(required=False, max_length=255, widget=forms.TextInput(
                                                        attrs={'class': 'form-control me-2', 'placeholder': 'Поиск'}),
                                   label='Ключевое слово')
    search_by = forms.ChoiceField(required=False, choices=SEARCH_OPTIONS,
                                                 widget=forms.Select(attrs={'class': 'form-control'}),
                                                 label='Искать по')
    order_by = forms.ChoiceField(required=False, choices=ORDER_BY,
                                           widget=forms.Select(attrs={'class': 'form-control'}), label='Сортировать по')