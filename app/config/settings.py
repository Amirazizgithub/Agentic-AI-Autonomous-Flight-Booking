"""Configuration management"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    # API Configuration
    app_name: str = "Agentic AI Flight Booking"
    app_version: str = "1.0.0"
    environment: str = "main"
    log_level: str = "INFO"
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # Agent Configuration
    max_iterations: int = 10
    agent_temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
