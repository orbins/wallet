import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object('config.settings.installed_apps')

app.autodiscover_tasks()
