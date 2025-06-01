import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bnpl.settings')

app = Celery('bnpl_celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-overdue-installments': {
        'task': 'apps.api.bg_tasks.installment_tasks.check_overdue_installments',
        'schedule': crontab(hour=0, minute=0),
    },
    'send-installment-reminders': {
        'task': 'apps.api.bg_tasks.installment_tasks.send_installment_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
