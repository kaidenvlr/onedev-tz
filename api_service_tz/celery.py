import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_service_tz.settings")
app = Celery("api_service_tz")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
