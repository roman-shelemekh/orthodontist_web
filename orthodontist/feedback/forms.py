from django import forms
from .models import Feedback
import re


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'comment', 'appointment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Электронный адрес'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Отзыв', 'style': 'height: 100px'})
        }
        labels = {
            'name': 'Имя',
            'email': 'Электронный адре',
            'comment': 'Отзыв'
        }

