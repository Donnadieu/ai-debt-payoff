"""Configuration management for the debt payoff API.

Production Integration Points:
This configuration module centralizes all environment-specific settings
required for production deployment. Key integration areas:

1. Database Configuration:
   - Production: PostgreSQL with connection pooling
   - Development: SQLite for local testing
   - Environment variable: DATABASE_URL

2. LLM API Integration:
   - OpenAI API key and endpoint configuration
   - Rate limiting and timeout settings
   - Environment variables: OPENAI_API_KEY, LLM_API_ENDPOINT

3. Redis Configuration:
   - Session storage and caching
   - Background job queue management
   - Environment variable: REDIS_URL

4. Security Settings:
   - CORS origins for frontend integration
   - JWT secret keys
   - Rate limiting configurations

5. Performance Monitoring:
   - Analytics endpoint configuration
   - Performance metrics collection
   - Environment variable: ANALYTICS_ENABLED
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Production Deployment Notes:
    - All sensitive values should be set via environment variables
    - Never commit API keys or secrets to version control
    - Use environment-specific .env files for configuration
    - Validate all required production settings on startup
    
    Required Production Environment Variables:
    - DATABASE_URL: Production PostgreSQL connection string
    - OPENAI_API_KEY: OpenAI API key for LLM integration
    - REDIS_URL: Redis connection string for caching/sessions
    - JWT_SECRET_KEY: Secret key for JWT token signing
    - CORS_ORIGINS: Comma-separated list of allowed origins
    """
    
    # Database Configuration
    # Production: Use PostgreSQL with connection pooling
    # Example: postgresql://user:password@localhost/debt_payoff
    # Development: SQLite for local testing
    database_url: str = "sqlite:///./debt_payoff.db"
    
    # API Configuration
    api_title: str = "AI Debt Payoff Planner API"
    api_version: str = "1.0.0"
    api_description: str = "API for managing debt payoff strategies with AI coaching"
    
    # LLM Integration - PRODUCTION INTEGRATION POINT
    # Required for AI coaching and nudge generation
    openai_api_key: Optional[str] = None  # Set via OPENAI_API_KEY env var
    llm_api_endpoint: str = "https://api.openai.com/v1"  # OpenAI endpoint
    llm_model: str = "gpt-3.5-turbo"  # Model for debt coaching
    llm_max_tokens: int = 500  # Token limit for responses
    llm_temperature: float = 0.7  # Creativity level for coaching messages
    
    # Environment Configuration
    environment: str = "development"  # Set to 'production' for deployment
    debug: bool = True  # Set to False for production
    
    # Redis Configuration - PRODUCTION INTEGRATION POINT
    # Required for session management and background job processing
    redis_url: Optional[str] = None  # Set via REDIS_URL env var
    redis_password: Optional[str] = None  # Redis authentication
    
    # Security Configuration - PRODUCTION INTEGRATION POINT
    jwt_secret_key: Optional[str] = None  # Set via JWT_SECRET_KEY env var
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours
    
    # Performance Monitoring - PRODUCTION INTEGRATION POINT
    analytics_enabled: bool = True  # Enable performance tracking
    max_debt_count: int = 10  # Performance limit
    calculation_timeout_ms: int = 500  # SLA requirement
    
    # CORS Configuration - PRODUCTION INTEGRATION POINT
    # Update for production frontend domains
    cors_origins: list[str] = [
        "http://localhost:3000",  # Local development
        "http://127.0.0.1:3000",  # Local development alt
        # Add production domains here:
        # "https://yourdomain.com",
        # "https://www.yourdomain.com"
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    def validate_production_settings(self) -> list[str]:
        """
        Validate required production configuration settings.
        
        Returns:
            List of missing configuration errors (empty if valid)
        """
        errors = []
        
        if self.environment == "production":
            # Required production settings
            if not self.openai_api_key:
                errors.append("OPENAI_API_KEY environment variable required for production")
            
            if not self.redis_url:
                errors.append("REDIS_URL environment variable required for production")
            
            if not self.jwt_secret_key:
                errors.append("JWT_SECRET_KEY environment variable required for production")
            
            if "sqlite" in self.database_url.lower():
                errors.append("Production requires PostgreSQL database, not SQLite")
            
            if self.debug:
                errors.append("DEBUG should be False in production environment")
        
        return errors


# Global settings instance
settings = Settings()

# Production validation check
# Uncomment for production deployment validation
# production_errors = settings.validate_production_settings()
# if production_errors:
#     raise ValueError(f"Production configuration errors: {production_errors}")
