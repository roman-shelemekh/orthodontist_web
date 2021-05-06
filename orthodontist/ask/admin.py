from django.contrib import admin
from .models import Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('title', 'date', 'author')
    list_filter = ['date']


admin.site.register(Question, QuestionAdmin)

