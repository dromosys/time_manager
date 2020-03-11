from celery import current_app
from time_app.models import time_entry
app = current_app._get_current_object()
from celery.schedules import crontab
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core import serializers
from django.urls import set_script_prefix
from django.conf import settings

log=get_task_logger(__name__)

def get_report_message(user):
    now = timezone.now()
    delta_days = 1;
    
    startdate = now - timedelta(days=delta_days)
    enddate = now + timedelta(days=1)
    
    te = time_entry.objects.filter(user_id=user, date__range=[startdate, enddate])
    sub_totals = time_entry.objects.values('name').filter(user_id=user, date__range=[startdate, enddate]).annotate(Sum('hours_worked'))
    
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
    
    log.info(context)  
      
    return context

@app.task
def email_report(name='mail_report'):
    print('email_report')
    
    subject='monthly report'
    from_email = 'admin@yourdomain.com'
    
    users = User.objects.all()
    
    for u in users:
        try:
        
            recipient_list=[str(u.email)]
            
            log.info(recipient_list)
            
            context = get_report_message(u)
            
            set_script_prefix(settings.SITE_URL)
            
            msg_html = render_to_string('email.html', context)
            
            message = 'test'
            
            send_mail(subject, message, from_email, recipient_list, html_message=msg_html) 
        
        except:
            log.error('error processing user_id:' + u.email) 
           
@app.on_after_finalize.connect
def app_ready(**kwargs):
    """
    Called once after app has been finalized.
    """
    sender = kwargs.get('sender')

    log.info('app_ready')
    # periodic tasks
    cron = crontab(minute=0, hour=12) #minute=0, hour=12
    sender.add_periodic_task(cron, email_report.s(),name='run task')
