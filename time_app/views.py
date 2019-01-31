from time_app.models import time_entry
from django.shortcuts import render, redirect, get_object_or_404
from time_app.forms import PostsForm
        
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

@login_required(login_url='/time/accounts/login/')
def list(request, template_name='list.html'):
    
    now = timezone.now()
    
    startdate = now - timedelta(days=7)
    enddate = now + timedelta(days=1)
    
    te = time_entry.objects.filter(author=request.user, date__range=[startdate, enddate])
    #data = {}
    #data['object_list'] = posts
    
    #.values > group by
    sub_totals = time_entry.objects.values('name').filter(author=request.user, date__range=[startdate, enddate]).annotate(Sum('hours_worked'))
    
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
    return render(request, template_name, context)

@login_required(login_url='/time/accounts/login/')
def edit(request, pk, template_name='edit.html'):
    post = get_object_or_404(time_entry, pk=pk, author=request.user)
    form = PostsForm(request.POST or None, instance=post)
    #print("get_timezone", request.session['django_timezone'])
    if form.is_valid():
        form.save()
        return redirect('time_app:list')
    return render(request, template_name, {'form': form})

@login_required(login_url='/time/accounts/login/')
def delete(request, pk, template_name='delete.html'):
    post = get_object_or_404(time_entry, pk=pk, author=request.user)
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
        form.instance.author = request.user
        form.save()
        return redirect('time_app:list')
    return render(request, template_name, {'form': form})

@login_required(login_url='/time/accounts/login/')
def getdata(request):
    results=time_entry.objects.filter(author=request.user)
    jsondata = serializers.serialize('json',results)
    return HttpResponse(jsondata)

@login_required(login_url='/time/accounts/login/')
def base_layout(request):
    template='base.html'
    return render(request,template)

from django.shortcuts import redirect, render

import pytz

@login_required(login_url='/time/accounts/login/')
def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        print("set_timezone", request.session['django_timezone'])
        return redirect('/time')
    else:
        return render(request, 'set_tz.html', {'timezones': pytz.common_timezones})