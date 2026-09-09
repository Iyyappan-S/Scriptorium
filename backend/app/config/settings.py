from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str
    VERSION: str

    MONGODB_URI: str
    DATABASE_NAME: str

    GEMINI_API_KEY: str | None = None

    NEO4J_URI: str | None = None
    NEO4J_USERNAME: str | None = None
    NEO4J_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        extra="ignore"
    )


settings = Settings()