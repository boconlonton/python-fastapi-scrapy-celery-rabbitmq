import os

from celery import Celery


celery_app = Celery(
    "worker",
    backend=os.getenv("CELERY_BACKEND_URL"),
    broker=os.getenv("CELERY_BROKER_URL"),
)

celery_app.conf.task_routes = {"worker.celery_worker.test_celery": "test-queue"}
celery_app.conf.update(task_track_started=True)
