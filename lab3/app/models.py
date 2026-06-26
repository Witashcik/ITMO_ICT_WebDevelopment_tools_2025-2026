from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class TaskTag(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None

    task: Optional["Task"] = Relationship(back_populates="tag_links")
    tag: Optional["Tag"] = Relationship(back_populates="task_links")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True

    tasks: list["Task"] = Relationship(back_populates="owner")
    categories: list["Category"] = Relationship(back_populates="owner")
    tags: list["Tag"] = Relationship(back_populates="owner")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="categories")

    tasks: list["Task"] = Relationship(back_populates="category")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    priority: str = Field(default="medium", index=True)
    status: str = Field(default="planned", index=True)
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="tasks")

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="tasks")

    time_entries: list["TimeEntry"] = Relationship(back_populates="task")
    tag_links: list[TaskTag] = Relationship(back_populates="task")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="tags")

    task_links: list[TaskTag] = Relationship(back_populates="tag")


class TimeEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    minutes: int = Field(gt=0)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    task_id: int = Field(foreign_key="task.id")
    task: Optional[Task] = Relationship(back_populates="time_entries")
