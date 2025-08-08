""" import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawlerserver.settings")

celery_app = Celery('gary')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
celery_app.conf.beat_schedule = {
 
    'workflow_update_from_vivid_mind_handler': {
        'task': 'crawl.external_party_communication_facilitator.create_workflow_from_payload',
        'schedule': crontab(minute='*/1'),
    },
}
 celery_app.conf.beat_schedule = {
 
    'create_logs': {
        'task': 'crawl.external_party_communication_facilitator.get_logs',
        'schedule': crontab(minute='*/1'),
    }, """

