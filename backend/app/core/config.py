"""
Configuration settings for ResumeAI Classifier
"""

import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "ResumeAI Classifier"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./resumeai.db"
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://resumeai-frontend.vercel.app"
    ]
    
    # AI/ML API settings
    GROK_API_KEY: str = ""
    GROK_API_URL: str = "https://api.x.ai"
    
    # Celery settings
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 