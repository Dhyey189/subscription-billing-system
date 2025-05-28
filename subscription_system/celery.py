import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subscription_system.settings")

app = Celery("subscription_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {}
