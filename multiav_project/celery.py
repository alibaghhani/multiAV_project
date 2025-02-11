import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multiav_project.settings")
app = Celery("multiav")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    task_concurrency=2,
    worker_prefetch_multiplier=1
)
app.autodiscover_tasks()
