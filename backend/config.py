"""Configuration management for the debt payoff API."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "sqlite:///./debt_payoff.db"
    
    # API
    api_title: str = "AI Debt Payoff Planner API"
    api_version: str = "1.0.0"
    api_description: str = "API for managing debt payoff strategies with AI coaching"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
