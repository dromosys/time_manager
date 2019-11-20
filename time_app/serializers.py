from django.contrib.auth.models import User
from .models import time_entry
from rest_framework import serializers

# https://www.django-rest-framework.org/api-guide/relations/

class UserSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
        
class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = time_entry
        fields = [ 'url', 'date', 'start_time', 'end_time', 'name', 'hours_break']