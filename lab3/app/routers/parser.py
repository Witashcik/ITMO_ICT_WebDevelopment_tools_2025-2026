import httpx
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.config import settings
from worker.celery_app import celery_app

router = APIRouter(prefix="/parser", tags=["parser"])


class ParseRequest(BaseModel):
    url: HttpUrl


@router.post("/parse")
def parse_via_http(data: ParseRequest):
    """Прямой вызов parser_service по HTTP."""
    try:
        response = httpx.post(
            f"{settings.parser_service_url}/parse",
            json={"url": str(data.url)},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.text,
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=500, detail=f"Parser service error: {exc}") from exc


@router.post("/parse-async")
def parse_via_queue(data: ParseRequest):
    """Асинхронный вызов парсера через Redis + Celery."""
    task = celery_app.send_task("worker.tasks.parse_url_task", args=[str(data.url)])
    return {
        "message": "Parsing task started",
        "task_id": task.id,
        "status_url": f"/parser/tasks/{task.id}",
    }


@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)

    return response
