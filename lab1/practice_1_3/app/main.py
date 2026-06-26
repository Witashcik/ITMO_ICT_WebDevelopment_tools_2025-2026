from fastapi import FastAPI

from app.routers import auth, categories, tags, tasks, time_entries, users

app = FastAPI(title="Time Manager API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(tags.router)
app.include_router(tasks.router)
app.include_router(time_entries.router)


@app.get("/")
def root():
    return {
        "message": "Time Manager API is running",
        "docs": "/docs",
    }
