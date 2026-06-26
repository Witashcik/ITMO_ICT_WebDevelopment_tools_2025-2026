from shared.parser import parse_url_and_save
from worker.celery_app import celery_app


@celery_app.task(name="worker.tasks.parse_url_task")
def parse_url_task(url: str) -> dict:
    return parse_url_and_save(url)
