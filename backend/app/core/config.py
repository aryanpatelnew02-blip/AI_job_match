from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgrespassword@localhost:5433/job_match_db"
    DATABASE_URL_TEST: str = "postgresql+psycopg://postgres:postgrespassword@localhost:5433/job_match_test_db"

    # Security & Auth
    ADMIN_API_KEY: str = "dev-admin-api-key-do-not-use-in-production"
    JWT_SECRET: str = "dev-jwt-secret-key-minimum-32-chars-long-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384

    # LLM Provider
    LLM_PROVIDER: str = "mock"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Ranking Weights
    RANKING_WEIGHT_SEMANTIC: float = 0.35
    RANKING_WEIGHT_SKILLS: float = 0.30
    RANKING_WEIGHT_EXPERIENCE: float = 0.20
    RANKING_WEIGHT_PREFERENCES: float = 0.15

    # Server & Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v


settings = Settings()
