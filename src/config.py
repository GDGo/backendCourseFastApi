import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import  Path


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # model_config = SettingsConfigDict(env_file=f"{Path(__file__).parent.parent / '.env'}")
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env"), extra="ignore"
    )


settings = Settings()