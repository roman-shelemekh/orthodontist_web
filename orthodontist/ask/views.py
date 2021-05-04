from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Count
from .models import Question, Answer
from .forms import AskQuestionForm, ReplyForm, OrderByForm
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import QuestionSerializer, QuestionEditSerializer



class AskView(TemplateView):
    template_name = 'ask/index.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = OrderByForm(request.GET)
        self.form.is_valid()
        return super(AskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AskView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


class QuestionDetail(DetailView):
    model = Question
    template_name = 'ask/question.html'
    context_object_name = 'question'

    def dispatch(self, request, *args, **kwargs):
        print(reverse('ask:question_ajax'))
        self.form = ReplyForm()
        return super(QuestionDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
        form = ReplyForm(request.POST)
        if form.is_valid():
            form.cleaned_data['question'] = Question.objects.get(id=kwargs['pk'])
            form.cleaned_data['author'] = request.user
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect(reverse('ask:question', args=(kwargs['pk'],)))

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context['reply_form'] = self.form
        return context


@method_decorator(login_required, name='dispatch')
class AskQuestionView(FormView):
    template_name = 'ask/ask_question.html'
    form_class = AskQuestionForm
    success_url = '/question/'

    def form_valid(self, form):
        form.cleaned_data['author'] = self.request.user
        form.save()
        return super().form_valid(form)


def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.user == question.author:
        _, deleted = question.delete()
        messages.success(
            request, f'Вопрос "{question.title}" и все ответы на него ({deleted.get("ask.Answer", "0")}) '
                     f'были успешно удалены'
        )
        return HttpResponseRedirect(reverse('ask:index'))
    else:
        raise Http404()


def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user == answer.author:
        answer.delete()
        messages.success(request, f'Ответ был успешно удален')
        return HttpResponseRedirect(reverse('ask:question', args=[answer.question.id]))
    else:
        raise Http404()


def like_question(request, pk):
    if request.is_ajax():
        user = request.user
        if user.is_authenticated:
            question = get_object_or_404(Question, pk=pk)
            if user not in question.like.all():
                question.like.add(user)
                add = True
            else:
                question.like.remove(user)
                add = False
            like_count = question.like.count()
            return JsonResponse({'like_count': like_count, 'add': add})
        else:
            return JsonResponse({'auth': '/login/?next=/question/'})
    else:
        raise Http404()


class QuestionListAjax(generics.ListAPIView):
    # TODO: check on is_ajax
    serializer_class = QuestionSerializer

    def get_queryset(self):
        order_by = self.request.GET.get('order_by')
        queryset = Question.objects.all().annotate(answers_count=Count('answer__id'))\
                                         .annotate(like_count=Count('like__id'))
        if not order_by or order_by == 'new':
            queryset = queryset.order_by('-date')
        elif order_by == 'old':
            queryset = queryset.order_by('date')
        elif order_by == 'popular':
            queryset = queryset.order_by('-like_count')
        elif order_by == 'answers':
            queryset = queryset.order_by('-answers_count')
        return queryset
    
    def get_serializer_context(self):
        context = super(QuestionListAjax, self).get_serializer_context()
        context['user'] = self.request.user
        return context


class QuestionEdit(APIView):

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        print(request.data)
        print(pk)
        question = self.get_object(pk)
        serializer = QuestionEditSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
