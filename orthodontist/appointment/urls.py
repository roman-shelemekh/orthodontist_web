from django.urls import path
from . import views


app_name = 'appointment'
urlpatterns = [
    path('', views.AppointmentView.as_view(), name='index'),
    path('get_clinics/', views.get_clinics, name='get_clinics'),
    path('get_dates/', views.get_dates, name='get_dates'),
    path('get_timetable/', views.get_timetable, name='get_timetable'),
    path('<int:pk>/delete_appointment/', views.delete_appointment, name='delete_appointment'),
    path('get_clinics_for_map/', views.ClinicsForMap.as_view(), name='get_clinics_for_map'),
]