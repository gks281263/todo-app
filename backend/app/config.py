from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///todo.db"
    log_level: str = "INFO"
    model_config = {"env_file": ".env"}


settings = Settings()
