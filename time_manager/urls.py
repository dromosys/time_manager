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
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers, serializers, viewsets
from time_app import views

app_name = 'time'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'time', views.TimeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^api/', include(router.urls)),

    url('', include('time_app.urls',  namespace='time')),
    
    url('', include('accounts.urls',  namespace='accounts')),
    
    url(r'^accounts/', include('django.contrib.auth.urls',namespace='')),
    
    url(r'^tz_detect/', include('tz_detect.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns