from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "To-Do List API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    model_config = {"env_file": ".env"}


settings = Settings()
