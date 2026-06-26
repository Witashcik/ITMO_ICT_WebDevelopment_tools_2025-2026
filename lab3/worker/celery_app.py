from celery import Celery

from shared.config import settings

celery_app = Celery(
    "time_manager_parser_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Tallinn",
    enable_utc=True,
)
