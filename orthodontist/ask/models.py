from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.CharField(max_length=1000)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    like = models.ManyToManyField(User, related_name='question_to_like')


    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text
