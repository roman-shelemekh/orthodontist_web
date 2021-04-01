from django import forms
from .models import Question, Answer

class AskQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вопрос кратко'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Подробное изложение вопроса'}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Вопрос'
        }

    def save(self, commit=True):
        question = Question(**self.cleaned_data)
        question.save()
        return question

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ваш ответ'}),
        }
        labels = {
            'text': 'Ответ'
        }

    def save(self, commit=True):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
