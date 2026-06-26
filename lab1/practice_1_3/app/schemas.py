from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool


class UserChangePassword(SQLModel):
    old_password: str
    new_password: str


class CategoryCreate(SQLModel):
    name: str
    description: Optional[str] = None


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int


class TagCreate(SQLModel):
    name: str


class TagUpdate(SQLModel):
    name: Optional[str] = None


class TagRead(SQLModel):
    id: int
    name: str
    owner_id: int


class TimeEntryCreate(SQLModel):
    minutes: int
    comment: Optional[str] = None


class TimeEntryUpdate(SQLModel):
    minutes: Optional[int] = None
    comment: Optional[str] = None


class TimeEntryRead(SQLModel):
    id: int
    minutes: int
    comment: Optional[str] = None
    created_at: datetime
    task_id: int


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "planned"
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None


class TaskRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    deadline: Optional[datetime] = None
    created_at: datetime
    owner_id: int
    category_id: Optional[int] = None


class TaskTagAttach(SQLModel):
    note: Optional[str] = None


class TaskTagRead(SQLModel):
    tag: TagRead
    assigned_at: datetime
    note: Optional[str] = None


class TaskReadFull(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    status: str
    deadline: Optional[datetime] = None
    created_at: datetime
    owner_id: int
    category: Optional[CategoryRead] = None
    tags: list[TaskTagRead] = []
    time_entries: list[TimeEntryRead] = []
