from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "cef39e20573ea328f91bdcccfbe1a91f93840535d53c63c0bf018ce608317242"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./bright_health.db"
    
    class Config:
        env_file = ".env"

settings = Settings()