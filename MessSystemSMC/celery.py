from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessSystemSMC.settings')

app = Celery('MessSystemSMC')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
