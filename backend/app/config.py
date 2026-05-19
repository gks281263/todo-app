import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:////tmp/todo.db" if os.environ.get("VERCEL") else "sqlite:///todo.db"
    log_level: str = "INFO"
    model_config = {"env_file": ".env"}


settings = Settings()
