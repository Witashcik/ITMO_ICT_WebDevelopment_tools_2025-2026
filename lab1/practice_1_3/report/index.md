# Отчёт по лабораторной работе

## Тема

Серверное приложение **Time Manager API** — программа для управления задачами, категориями, тегами и учётом затраченного времени.

## Используемые технологии

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLModel
- Alembic
- JWT
- Passlib / bcrypt

## Модели базы данных

В проекте реализованы таблицы:

1. `user` — пользователь системы.
2. `category` — категория задач.
3. `task` — задача пользователя.
4. `tag` — тег задачи.
5. `tasktag` — ассоциативная таблица для связи задач и тегов.
6. `timeentry` — запись времени, затраченного на задачу.

## Связи

- `user -> task` — one-to-many.
- `user -> category` — one-to-many.
- `category -> task` — one-to-many.
- `task -> timeentry` — one-to-many.
- `task <-> tag` — many-to-many через `tasktag`.

Ассоциативная таблица `tasktag` содержит дополнительные поля:

- `assigned_at` — дата прикрепления тега к задаче;
- `note` — заметка к связи задачи и тега.

## Основные эндпоинты

### Авторизация

- `POST /auth/register` — регистрация.
- `POST /auth/login` — вход и получение JWT.

### Пользователи

- `GET /users/me` — текущий пользователь.
- `GET /users` — список пользователей.
- `PUT /users/change-password` — смена пароля.

### Категории

- `POST /categories`
- `GET /categories`
- `GET /categories/{category_id}`
- `PUT /categories/{category_id}`
- `DELETE /categories/{category_id}`

### Теги

- `POST /tags`
- `GET /tags`
- `GET /tags/{tag_id}`
- `PUT /tags/{tag_id}`
- `DELETE /tags/{tag_id}`

### Задачи

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- `POST /tasks/{task_id}/tags/{tag_id}`
- `DELETE /tasks/{task_id}/tags/{tag_id}`

### Учёт времени

- `POST /tasks/{task_id}/time-entries`
- `GET /tasks/{task_id}/time-entries`
- `PUT /time-entries/{entry_id}`
- `DELETE /time-entries/{entry_id}`

## Подключение к базе данных

Код подключения находится в файле `app/database.py`.

```python
from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(settings.database_url, echo=False)


def get_session():
    with Session(engine) as session:
        yield session
```

## Переменные окружения

Пример находится в файле `.env.example`.

```text
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/time_manager_db
SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Миграции

Миграции Alembic находятся в папке `migrations`.

Основная команда применения миграций:

```bash
alembic upgrade head
```

## Проверка

Swagger-документация доступна по адресу:

```text
http://127.0.0.1:8000/docs
```
