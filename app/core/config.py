from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_title: str = 'Кошелёк'
    database_url: str = 'sqlite+aiosqlite:///./test.db'

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
