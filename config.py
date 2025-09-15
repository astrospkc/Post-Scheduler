from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App settings
    app_name: str = "FastAPI Neon SQLAlchemy"
    debug: bool = False
    secret_key: str = "your-secret-key-change-this"
    
    # Database settings
    database_url: str
    db_pool_size: int = 20
    db_max_overflow: int = 30
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()