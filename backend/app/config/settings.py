from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "AI Multi-Agent Academic Research Platform"
    VERSION: str = "1.0.0"

    MONGODB_URI: str = "mongodb+srv://vsbiyyappan2005_db_user:Research12345@finwisecluster.wzjmfjj.mongodb.net/?appName=FinWiseCluster"
    DATABASE_NAME: str = "research_platform"

    GEMINI_API_KEY: str | None = None

    NEO4J_URI: str | None = None
    NEO4J_USERNAME: str | None = None
    NEO4J_PASSWORD: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
