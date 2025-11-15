from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sistema_academico"

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistema Académico API"
    VERSION: str = "1.0.0"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
