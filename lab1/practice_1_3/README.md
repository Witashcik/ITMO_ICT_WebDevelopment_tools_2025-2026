# Практика 1.3 / Финальный проект

Тема: **программа-тайм-менеджер**.

Реализовано:

- FastAPI;
- PostgreSQL;
- SQLModel;
- Alembic;
- CRUD;
- JWT-авторизация;
- хэширование паролей;
- 6 таблиц;
- one-to-many;
- many-to-many;
- ассоциативная таблица `tasktag` с дополнительными полями `assigned_at` и `note`.

## Таблицы

- `user` — пользователи;
- `category` — категории задач;
- `task` — задачи;
- `tag` — теги;
- `tasktag` — связь задач и тегов;
- `timeentry` — записи времени по задачам.

## Запуск на Windows в VS Code

Откройте папку `practice_1_3` в VS Code.

Создать виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Если PowerShell ругается на запуск скриптов:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Установить зависимости:

```powershell
pip install -r requirements.txt
```

Создать `.env`:

```powershell
copy .env.example .env
```

Запустить PostgreSQL:

```powershell
docker compose up -d
```

Применить миграции:

```powershell
alembic upgrade head
```

Запустить сервер:

```powershell
uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Проверка в Swagger

1. `POST /auth/register` — зарегистрировать пользователя.
2. `POST /auth/login` — войти и получить токен.
3. Нажать кнопку **Authorize** в Swagger и вставить токен.
4. `POST /categories` — создать категорию.
5. `POST /tags` — создать тег.
6. `POST /tasks` — создать задачу.
7. `POST /tasks/{task_id}/tags/{tag_id}` — прикрепить тег к задаче.
8. `POST /tasks/{task_id}/time-entries` — добавить запись времени.
9. `GET /tasks/{task_id}` — получить задачу с вложенными объектами.
