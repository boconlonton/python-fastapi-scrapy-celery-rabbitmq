import os
import sys

from celery import Celery


app = Celery('celery_tasks')

app.config_from_object('celeryconfig')
