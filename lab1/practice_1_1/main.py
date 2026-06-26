from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Practice 1.1 - Time Manager")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None


class TaskRead(TaskCreate):
    id: int
    is_completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None


# Временная база данных в памяти
fake_tasks_db: list[TaskRead] = []
next_task_id = 1


@app.get("/")
def root():
    return {"message": "Time Manager API. Open /docs"}


@app.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    global next_task_id

    new_task = TaskRead(id=next_task_id, **task.model_dump())
    fake_tasks_db.append(new_task)
    next_task_id += 1
    return new_task


@app.get("/tasks", response_model=list[TaskRead])
def get_tasks():
    return fake_tasks_db


@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    for task in fake_tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate):
    for index, task in enumerate(fake_tasks_db):
        if task.id == task_id:
            updated_data = task.model_dump()
            updated_data.update(task_update.model_dump(exclude_unset=True))
            updated_task = TaskRead(**updated_data)
            fake_tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(fake_tasks_db):
        if task.id == task_id:
            fake_tasks_db.pop(index)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
