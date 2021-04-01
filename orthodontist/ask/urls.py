from django.urls import path

from . import views


app_name = 'ask'
urlpatterns = [
    path('', views.AskView.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='question'),
    path('ask_question', views.AskQuestionView.as_view(), name='ask_question'),
    path('<int:pk>/delete_question', views.delete_question, name='delete_question'),
    path('<int:pk>/delete_answer', views.delete_answer, name='delete_answer'),
]