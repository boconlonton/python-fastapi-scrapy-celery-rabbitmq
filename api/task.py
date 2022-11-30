from fastapi import APIRouter, Body

from fastapi.responses import JSONResponse

from celery.result import AsyncResult

from worker.tasks import crawler_task

tasks_api = APIRouter()

@tasks_api.post('/', status_code=201)
def run_task():
    for _ in range(100):
        task = crawler_task.delay(157991)

    return JSONResponse({
        "task_id": task.id
    })

@tasks_api.get("/{task_id}")
def get_task(task_id: str):

    task_result = AsyncResult(task_id)

    return JSONResponse({
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    })
