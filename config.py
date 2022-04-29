from functools import lru_cache
from pydantic import BaseSettings


class Config(BaseSettings):
    app_title: str = "IREEN API"
    app_version: str = "3.1.2"
    app_description: str = "Part 1: Backend Test"
    db_path: str
    access_token_expire_minutes: int = 60 * 24 * 8
    # 60 minutes * 24 hours * 8 days = 8 days
    class Config:
        env_file = ".env"

settings = Config()

@lru_cache()
def get_config():
    return Config()


