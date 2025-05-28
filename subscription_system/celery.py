import os
from celery import Celery, signals
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subscription_system.settings")

app = Celery("subscription_system")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "generate_invoices": {
        "task": "subscriptions.tasks.task_generate_invoices",
        "schedule": crontab(minute=0, hour=0),
    },
    "mark_invoices_overdue": {
        "task": "subscriptions.tasks.task_mark_invoices_overdue",
        "schedule": crontab(minute=30, hour=0),
    },
    "send_invoice_reminders": {
        "task": "subscriptions.tasks.task_send_invoice_reminders",
        "schedule": crontab(minute=0, hour=1),
    },
}


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass
