"""time_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
    
    http://localhost:8000/accounts/login/
    http://localhost:8000/
    
"""
from django.conf.urls import include, url
from django.contrib import admin
from time_app import views
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import auth_logout, auth_login

app_name = 'time_app'

urlpatterns = [

    url(r'^$', views.list, name='list'),
    url(r'^edit/(?P<pk>\d+)$', views.edit, name='edit'),
    url(r'^new$', views.create, name='new'),
    url(r'^delete/(?P<pk>\d+)$', views.delete, name='delete'),
    url(r'^set_timezone$', views.set_timezone, name='set_timezone'),
    
    url(r'^accounts/register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'),
    url(r'^accounts/', include('django_registration.backends.one_step.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    
    url(r'base_layout',views.base_layout,name='base_layout'),
    url(r'getdata',views.getdata,name='getdata'),
    url('', include('pwa.urls')),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
