from django.forms import ModelForm
from django import forms
from time_app.models import time_entry
#from django.contrib.admin import widgets  
from django.forms.widgets import NumberInput

# https://stackoverflow.com/questions/3367091/whats-the-cleanest-simplest-to-get-running-datepicker-in-django

class DeltaForm(forms.Form):
    delta_days = forms.IntegerField(label='Days',min_value=0)

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class PostsForm(ModelForm):
    class Meta:
        model = time_entry
        fields = ['name', 'date','start_time', 'end_time', 'hours_break']
        widgets = {
            'date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput(),
            'hours_break': NumberInput()
        }