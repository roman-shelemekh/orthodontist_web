from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.CharField(max_length=1000, verbose_name='Текст вопроса')
    title = models.CharField(max_length=255, verbose_name='Заголовок вопроса')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Автор')
    like = models.ManyToManyField(User, related_name='question_to_like',
                                  verbose_name='Пользователи, которым нравится вопрос')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    text = models.CharField(max_length=1000, verbose_name='Текст ответа')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Автор')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'Ответы'
