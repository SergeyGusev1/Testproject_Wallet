from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кошелёк'
    database_url: str = 'sqlite+aiosqlite:///./test.db'

    class Config:
        env_file = '.env'


settings = Settings()
