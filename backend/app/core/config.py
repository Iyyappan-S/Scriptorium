from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):

    PROJECT_NAME: str = "AI Multi-Agent Academic Research Platform"

    VERSION: str = "1.0.0"

    MONGODB_URI: str = ""

    DATABASE_NAME: str = "research_platform"

    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
