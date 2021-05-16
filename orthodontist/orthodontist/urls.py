"""orthodontist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from index import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('question/', include('ask.urls')),
    path('appointment/', include('appointment.urls')),
    path('feedback/', include('feedback.urls')),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('user/<int:pk>/popular/', views.UserViewPopular.as_view(), name='user_popular'),
    path('user/<int:pk>/update/', views.UserViewUpdate.as_view(), name='update'),
    path('user/<int:pk>/appointments/', views.UserViewAppointments.as_view(), name='appointments'),
    path('search/', views.SearchResults.as_view(), name='search'),

]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)