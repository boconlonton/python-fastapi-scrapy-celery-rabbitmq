import os

import sys

from celery import Celery


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(CURRENT_DIR)


celery_app = Celery("worker")

celery_app.config_from_object('celeryconfig')
