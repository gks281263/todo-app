import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:////tmp/todo.db" if os.environ.get("VERCEL") else "sqlite:///todo.db"
    log_level: str = "INFO"
    secret_key: str = "super-secret-default-key-please-change-in-prod"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    model_config = {"env_file": ".env"}


settings = Settings()

