from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "YouTube Channel Chatbot"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    DATABASE_URL: str = "sqlite:///./test.db"
    
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    YOUTUBE_API_KEY: str = Field(..., env="YOUTUBE_API_KEY")
    
    VECTOR_STORE_PATH: str = "./vector_index"
    TOP_K_RESULTS: int = 5
    
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100
    
    # Use pydantic-settings v2 style model config so the env_file is applied
    # parents[2] => repository root (../.. from this file: app/core/config.py)
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
    