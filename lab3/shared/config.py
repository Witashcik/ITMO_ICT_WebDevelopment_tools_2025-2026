from pydantic_settings import BaseSettings, SettingsConfigDict


class SharedSettings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@db:5432/time_manager_db"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = SharedSettings()
