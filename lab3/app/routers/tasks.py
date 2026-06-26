from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.database import get_session
from app.dependencies import get_current_user
from app.models import Category, Tag, Task, TaskTag, TimeEntry, User
from app.schemas import (
    CategoryRead,
    TagRead,
    TaskCreate,
    TaskRead,
    TaskReadFull,
    TaskTagAttach,
    TaskTagRead,
    TaskUpdate,
    TimeEntryRead,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


def task_to_full_read(task: Task) -> TaskReadFull:
    category = None
    if task.category is not None:
        category = CategoryRead(
            id=task.category.id,
            name=task.category.name,
            description=task.category.description,
            owner_id=task.category.owner_id,
        )

    tags = []
    for link in task.tag_links:
        if link.tag is not None:
            tags.append(
                TaskTagRead(
                    tag=TagRead(
                        id=link.tag.id,
                        name=link.tag.name,
                        owner_id=link.tag.owner_id,
                    ),
                    assigned_at=link.assigned_at,
                    note=link.note,
                )
            )

    time_entries = [
        TimeEntryRead(
            id=entry.id,
            minutes=entry.minutes,
            comment=entry.comment,
            created_at=entry.created_at,
            task_id=entry.task_id,
        )
        for entry in task.time_entries
    ]

    return TaskReadFull(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        deadline=task.deadline,
        created_at=task.created_at,
        owner_id=task.owner_id,
        category=category,
        tags=tags,
        time_entries=time_entries,
    )


def get_owned_task(task_id: int, current_user: User, session: Session) -> Task:
    task = session.get(Task, task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if data.category_id is not None:
        category = session.get(Category, data.category_id)
        if category is None or category.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Category not found")

    task = Task(**data.model_dump(), owner_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("", response_model=list[TaskRead])
def get_tasks(
    status_filter: str | None = Query(default=None, alias="status"),
    priority: str | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = select(Task).where(Task.owner_id == current_user.id)

    if status_filter is not None:
        statement = statement.where(Task.status == status_filter)
    if priority is not None:
        statement = statement.where(Task.priority == priority)

    return session.exec(statement).all()


@router.get("/{task_id}", response_model=TaskReadFull)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    statement = (
        select(Task)
        .where(Task.id == task_id, Task.owner_id == current_user.id)
        .options(
            selectinload(Task.category),
            selectinload(Task.time_entries),
            selectinload(Task.tag_links).selectinload(TaskTag.tag),
        )
    )
    task = session.exec(statement).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_to_full_read(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)

    if data.category_id is not None:
        category = session.get(Category, data.category_id)
        if category is None or category.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Category not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)

    links = session.exec(select(TaskTag).where(TaskTag.task_id == task.id)).all()
    for link in links:
        session.delete(link)

    entries = session.exec(select(TimeEntry).where(TimeEntry.task_id == task.id)).all()
    for entry in entries:
        session.delete(entry)

    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}


@router.post("/{task_id}/tags/{tag_id}")
def add_tag_to_task(
    task_id: int,
    tag_id: int,
    data: TaskTagAttach | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)
    tag = session.get(Tag, tag_id)
    if tag is None or tag.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")

    existing_link = session.get(TaskTag, (task.id, tag.id))
    if existing_link is not None:
        raise HTTPException(status_code=400, detail="Tag already attached to task")

    link = TaskTag(
        task_id=task.id,
        tag_id=tag.id,
        note=data.note if data is not None else None,
    )
    session.add(link)
    session.commit()
    return {"message": "Tag attached to task"}


@router.delete("/{task_id}/tags/{tag_id}")
def remove_tag_from_task(
    task_id: int,
    tag_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = get_owned_task(task_id, current_user, session)
    tag = session.get(Tag, tag_id)
    if tag is None or tag.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")

    link = session.get(TaskTag, (task.id, tag.id))
    if link is None:
        raise HTTPException(status_code=404, detail="Task tag link not found")

    session.delete(link)
    session.commit()
    return {"message": "Tag removed from task"}
