from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from .models import Question, Answer
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from .forms import AskQuestionForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib import messages


def index(request):
    question_list = Question.objects.order_by('-date')
    return render(request, 'ask/index.html', {'question_list': question_list})


class AskView(ListView):
    model = Question
    template_name = 'ask/index.html'

    def get_queryset(self):
        queryset = Question.objects.order_by('-date')
        queryset = queryset.annotate(answers_count=Count('answer__id'))
        return queryset


class QuestionDetail(DetailView):
    model = Question
    template_name = 'ask/question.html'
    context_object_name = 'question'

    def dispatch(self, request, *args, **kwargs):
        self.form = ReplyForm()
        return super(QuestionDetail, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
    success_url = '/ask/'


    def form_valid(self, form):
        form.cleaned_data['author'] = self.request.user
        print(form.cleaned_data)
        form.save()
        return super().form_valid(form)


def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    _, deleted = question.delete()
    messages.success(
        request, f'Вопрос "{question.title}" и все ответы на него ({deleted.get("ask.Answer")}) были успешно удалены'
    )
    return HttpResponseRedirect(reverse('ask:index'))


def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    messages.success(request, f'Ответ был успешно удален')
    return HttpResponseRedirect(reverse('ask:question', args=[answer.question.id]))