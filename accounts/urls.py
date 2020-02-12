# accounts/urls.py
from django.urls import path
from django.conf.urls import include, url
from . import views
from django.contrib.auth import views
from django_registration.backends.one_step.views import RegistrationView

app_name = 'accounts'

urlpatterns = [

    url(r'^accounts/register/', RegistrationView.as_view(success_url='/time'), name='django_registration_register'),
    
    url(r'^accounts/', include('django_registration.backends.one_step.urls')),
    
    #url(r'^accounts/', include('django.contrib.auth.urls',namespace='')),
]