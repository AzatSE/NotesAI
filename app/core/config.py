from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

from typing import List


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXP_DAYS: int
    SECRET_KEY: str

    @property
    def URL_DB(self) -> str:
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = str(Path(__file__).parents[2] / ".env")
        env_file_encoding = "utf-8"

settings = Settings()

@lru_cache
def get_settings(self):
    return Settings()