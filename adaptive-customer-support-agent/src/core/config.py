"""
Centralised configuration using Pydantic settings.
• Reads environment variables (via .env) once at startup
• Cached to avoid repeated disk IO
• Provides defaults for local development
"""
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # --------------------------------------------------------------------- #
    # LLM / OpenAI
    # --------------------------------------------------------------------- #
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_api_base: str | None = Field(None, env="OPENAI_API_BASE")

    # --------------------------------------------------------------------- #
    # Databases
    # --------------------------------------------------------------------- #
    mongodb_uri: str = Field(..., env="MONGODB_URI")
    mongodb_database: str = Field("adaptive_support", env="MONGODB_DATABASE")

    redis_url: str | None = Field("redis://localhost:6379", env="REDIS_URL")

    vector_store: str = Field("faiss", env="VECTOR_STORE")
    vector_directory: str = Field("./src/data/faiss_index", env="VECTOR_DIRECTORY")

    # --------------------------------------------------------------------- #
    # Agent behaviour
    # --------------------------------------------------------------------- #
    max_history_messages: int = 15
    similarity_top_k: int = 4

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    # Cached settings instance – safe to import anywhere
    return Settings()


settings: Settings = get_settings()
