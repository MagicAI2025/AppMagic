from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    
    # Security configuration
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI configuration
    OPENAI_API_KEY: str
    
    # DeepSeek configuration
    DEEPSEEK_API_KEY: str
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    DEFAULT_LLM_MODEL: str = "deepseek-coder-33b-instruct"  # or gpt-4-turbo-preview
    
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 80
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings() 