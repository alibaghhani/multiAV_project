import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "multiav_project.settings")
app = Celery("multiav")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()