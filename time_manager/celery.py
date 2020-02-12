import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'time_manager.settings')

app = Celery('time_manager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()