from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import Task, TimeEntry, User
from app.schemas import TimeEntryCreate, TimeEntryRead, TimeEntryUpdate

router = APIRouter(tags=["time entries"])


def get_owned_task(task_id: int, current_user: User, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post(
    "/tasks/{task_id}/time-entries",
    response_model=TimeEntryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_time_entry(
    task_id: int,
    data: TimeEntryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)

    entry = TimeEntry(**data.model_dump(), task_id=task.id)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.get("/tasks/{task_id}/time-entries", response_model=list[TimeEntryRead])
def get_task_time_entries(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)
    return session.exec(select(TimeEntry).where(TimeEntry.task_id == task.id)).all()


@router.put("/time-entries/{entry_id}", response_model=TimeEntryRead)
def update_time_entry(
    entry_id: int,
    data: TimeEntryUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    entry = session.get(TimeEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")

    task = session.get(Task, entry.task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Time entry not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)

    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.delete("/time-entries/{entry_id}")
def delete_time_entry(
    entry_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    entry = session.get(TimeEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Time entry not found")

    task = session.get(Task, entry.task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Time entry not found")

    session.delete(entry)
    session.commit()
    return {"message": "Time entry deleted"}
