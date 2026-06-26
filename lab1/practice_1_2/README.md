# Практика 1.2

FastAPI + PostgreSQL + SQLModel. Здесь база создаётся автоматически через `SQLModel.metadata.create_all()`.

## Запуск

```powershell
copy .env.example .env
pip install -r requirements.txt
docker compose up -d
uvicorn main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```
