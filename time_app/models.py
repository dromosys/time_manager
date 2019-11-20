from django.db import models
#from django.contrib.auth.models import User

#from django_currentuser.middleware import (
#    get_current_user, get_current_authenticated_user)
#from django_currentuser.db.models import CurrentUserField

#https://docs.djangoproject.com/en/2.1/topics/auth/customizing/
from django.conf import settings
#from django.db.models.signals import post_save
from datetime import timedelta
#from datetime import datetime 
from django.utils import timezone

def now_round_min(): 
    #print(timezone.now().replace(second=0, microsecond=0))
    return timezone.localtime(timezone.now()).replace(second=0, microsecond=0) 

def now_round_hour_min():
    return timezone.localtime(timezone.now()).replace(second=0,minute=0, microsecond=0)+timedelta(hours=2)
    #return now().replace(second=0,minute=0, microsecond=0)+timedelta(hours=2)
    
# Create your models here.
class time_entry(models.Model):

    print("timezone.now",timezone.now)
    
    date = models.DateField(default=timezone.now)
    start_time =  models.TimeField(default=now_round_min)
    end_time = models.TimeField(default=now_round_hour_min)
    name = models.CharField(max_length=200)
    #https://wsvincent.com/django-referencing-the-user-model/
    #created_by = CurrentUserField()
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hours_break = models.FloatField(default=0)
    hours_worked = models.FloatField(default=0)
    
    def __str__(self):
        return self.name
    
    @property
    def duration(self):
        end = timedelta(hours=self.end_time.hour, minutes=self.end_time.minute, seconds=self.end_time.second)
        start = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute, seconds=self.start_time.second)
        
        return ((end - start).seconds - self.hours_break*3600) / 3600
    
    def save(self,*args,**kwargs):
        self.hours_worked = self.duration
        super().save(*args, **kwargs)
        
class time_summary(time_entry):
    class Meta:
        proxy = True
        verbose_name = "Time Summary"
        verbose_name_plural = "Times Summary"