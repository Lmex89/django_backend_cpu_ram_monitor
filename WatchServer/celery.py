import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WatchServer.settings")

app = Celery("WatchServer", broker="redis://redis:6379")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "core_temps": {
        # run this task every minute
        "task": "temps.tasks.create_data_temps_cpu",
        "schedule": crontab(minute="*/1"),
    },
    "core_loads": {
        # run this task every minute
        "task": "temps.tasks.create_data_cpu_load",
        "schedule": crontab(minute="*/1"),
    },
}
