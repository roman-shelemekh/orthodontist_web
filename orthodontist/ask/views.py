from django.shortcuts import render

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Question, Answer


def index(request):
    question_list = Question.objects.order_by('-date')
    return render(request, 'ask/index.html', {'question_list': question_list})


def detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    return render(request, 'ask/question.html', {'question': question})
