from functools import lru_cache
from pydantic_settings import BaseSettings
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
    