from django import forms
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta
from .models import Profile


class SignupForm(UserCreationForm):
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type': 'checkbox'}), label='Запомнить меня',
                                     required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].widget.attrs['placeholder'] = 'Электронный адрес*'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя*'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль*'
        self.fields['password1'].help_text = 'Ваш пароль должен содержать как минимум 8 символов и не может ' \
                                             'состоять только из цифр'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль*'

    def log_in(self, request, user):
        login(request, user)
        if self.cleaned_data['remember_me']:
            request.session.set_expiry(timedelta(days=30).total_seconds())
        else:
            request.session.set_expiry(0)

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data['first_name'] + str(timezone.now().timestamp().__trunc__())
        if commit:
            user.save()
        return user

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('Поле "Имя" является обязательным для заполнения.')
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if email in User.objects.all().values_list('email', flat=True):
            raise forms.ValidationError('Пользователь с таким электронным адресом уже существует.')
        return email


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронная почта'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                             'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'type': 'checkbox'}), label='Запомнить меня',
                                     required=False)

    def log_in(self, request):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        remember_me = self.cleaned_data['remember_me']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if remember_me:
                request.session.set_expiry(timedelta(days=30).total_seconds())
            else:
                request.session.set_expiry(0)
            return True


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['type'] = 'email'
        self.fields['email'].widget.attrs['placeholder'] = 'Электронный адрес*'

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('Поле "Имя" является обязательным для заполнения.')
        return first_name


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
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Искать по')
    order_by = forms.ChoiceField(required=False, choices=ORDER_BY,
                                 widget=forms.Select(attrs={'class': 'form-control'}), label='Сортировать по')
