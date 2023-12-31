import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.settings')

app = Celery('settings')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'apps.goals.tasks.calculate_daily_percent',
        'schedule': crontab(minute='0', hour='0'),
    }
}
