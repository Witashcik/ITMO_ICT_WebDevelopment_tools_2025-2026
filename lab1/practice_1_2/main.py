import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/time_manager_db",
)

engine = create_engine(DATABASE_URL, echo=True)
app = FastAPI(title="Practice 1.2 - Time Manager with PostgreSQL")


class TaskTag(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = None


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None

    tasks: list["Task"] = Relationship(back_populates="category")


class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTag)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None
    is_completed: bool = False

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="tasks")

    tags: list[Tag] = Relationship(back_populates="tasks", link_model=TaskTag)


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None
    category_id: Optional[int] = None


class CategoryCreate(SQLModel):
    name: str
    description: Optional[str] = None


class TagCreate(SQLModel):
    name: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def root():
    return {"message": "Practice 1.2. Open /docs"}


@app.post("/categories", response_model=Category)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/categories", response_model=list[Category])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


@app.post("/tags", response_model=Tag)
def create_tag(tag: TagCreate, session: Session = Depends(get_session)):
    db_tag = Tag.model_validate(tag)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag


@app.get("/tags", response_model=list[Tag])
def get_tags(session: Session = Depends(get_session)):
    return session.exec(select(Tag)).all()


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    if task.category_id is not None:
        category = session.get(Category, task.category_id)
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")

    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[Task])
def get_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}


@app.post("/tasks/{task_id}/tags/{tag_id}")
def add_tag_to_task(task_id: int, tag_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    task.tags.append(tag)
    session.add(task)
    session.commit()
    return {"message": "Tag added to task"}
