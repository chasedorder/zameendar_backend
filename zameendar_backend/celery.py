from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

from zameendar_backend.settings import base

if base.DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zameendar_backend.settings.dev")
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "zameendar_backend.settings.production"
    )

app = Celery("zameendar_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
