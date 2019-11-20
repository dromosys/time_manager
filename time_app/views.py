from time_app.models import time_entry
from django.shortcuts import render, redirect, get_object_or_404
from time_app.forms import PostsForm
from .serializers import UserSerializer
        
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .forms import DeltaForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
import pytz
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User, Group
from .permissions import IsAccountAdmin
from .serializers import TimeSerializer

@login_required(login_url='/time/accounts/login/')
def list(request, template_name='list.html'):
    
    now = timezone.now()
    delta_days = 1;
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeltaForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            delta_days = form.cleaned_data['delta_days']

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DeltaForm()
    
    startdate = now - timedelta(days=delta_days)
    enddate = now + timedelta(days=1)
    
    te = time_entry.objects.filter(user_id=request.user, date__range=[startdate, enddate])
    #data = {}
    #data['object_list'] = posts
    
    #.values > group by
    sub_totals = time_entry.objects.values('name').filter(user_id=request.user, date__range=[startdate, enddate]).annotate(Sum('hours_worked'))
    
    total = 0
    for time in te:
        total += time.duration       
    
    jsondata = serializers.serialize('json',te)
    
    context={
        'results':te,
        'sub_totals': sub_totals,
        'jsondata':jsondata,
        'total':total,
    }
    
    #print(sub_totals)
    
    #return render(request, template_name, data, context)
    return render(request, template_name, context, {'form': form})

@login_required(login_url='/time/accounts/login/')
def edit(request, pk, template_name='edit.html'):
    post = get_object_or_404(time_entry, pk=pk, user_id=request.user)
    form = PostsForm(request.POST or None, instance=post)
    #print("get_timezone", request.session['django_timezone'])
    if form.is_valid():
        form.save()
        return redirect('time_app:list')
    return render(request, template_name, {'form': form})

@login_required(login_url='/time/accounts/login/')
def delete(request, pk, template_name='delete.html'):
    post = get_object_or_404(time_entry, pk=pk, user_id=request.user)
    if request.method=='POST':
        post.delete()
        return redirect('time_app:list')
    return render(request, template_name, {'object': post})

@login_required(login_url='/time/accounts/login/')
def create(request, template_name='edit.html'):
    form = PostsForm(request.POST or None)
    
    if 'django_timezone' not in request.session:
        print("views.django_timezone not set")  
    else :
        print("views.get_timezone", request.session['django_timezone'])    
    
    if form.is_valid():
        form.instance.user_id = request.user
        form.save()
        return redirect('time_app:list')
    return render(request, template_name, {'form': form})

@login_required(login_url='/time/accounts/login/')
def getdata(request):
    results=time_entry.objects.filter(user_id=request.user)
    jsondata = serializers.serialize('json',results)
    return HttpResponse(jsondata)

@login_required(login_url='/time/accounts/login/')
def base_layout(request):
    template='base.html'
    return render(request,template)

@login_required(login_url='/time/accounts/login/')
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        print("set_timezone", request.session['django_timezone'])
        return redirect('/time')
    else:
        return render(request, 'set_tz.html', {'timezones': pytz.common_timezones})
    
class BaseViewSet (viewsets.ModelViewSet ):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        qs = self.queryset.filter(user_id=self.request.user)
        return qs
    def perform_create(self, serializer):
        serializer.save(user_id = self.request.user)
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAccountAdmin]

class TimeViewSet(BaseViewSet):
    queryset = time_entry.objects.all().order_by('name')
    serializer_class = TimeSerializer