from django.urls import path

from . import views
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'ask'
urlpatterns = [
    path('', views.AskView.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='question'),
    path('ask/', views.AskQuestionView.as_view(), name='ask_question'),
    path('<int:pk>/delete_question/', views.delete_question, name='delete_question'),
    path('<int:pk>/delete_answer/', views.delete_answer, name='delete_answer'),
    path('<int:pk>/like/', views.like_question, name='like'),
    path('ajax_sorting/', views.QuestionListAjax.as_view(), name='question_ajax')
]

# urlpatterns += format_suffix_patterns([path('ajax_sorting/', views.QuestionListAjax.as_view(), name='question_ajax')])