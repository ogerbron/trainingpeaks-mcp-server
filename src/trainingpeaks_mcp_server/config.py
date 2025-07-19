"""Configuration management for TrainingPeaks MCP server."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TrainingPeaksConfig(BaseSettings):
    """TrainingPeaks API configuration."""
    
    client_id: Optional[str] = Field(default=None, env="TRAININGPEAKS_CLIENT_ID")
    client_secret: Optional[str] = Field(default=None, env="TRAININGPEAKS_CLIENT_SECRET")
    redirect_uri: str = Field(
        default="http://localhost:8080/callback", 
        env="TRAININGPEAKS_REDIRECT_URI"
    )
    scopes: str = Field(
        default="athlete:profile,athlete:workouts", 
        env="TRAININGPEAKS_SCOPES"
    )
    environment: str = Field(default="sandbox", env="TRAININGPEAKS_ENVIRONMENT")
    
    class Config:
        env_file = ".env"
        validate_assignment = True
        extra = "ignore"
    
    @property
    def api_base_url(self) -> str:
        """Get the appropriate API base URL based on environment."""
        if self.environment == "production":
            return "https://api.trainingpeaks.com"
        return "https://sandbox-api.trainingpeaks.com"
    
    @property
    def auth_url(self) -> str:
        """Get the authorization URL."""
        return f"{self.api_base_url}/oauth/authorize"
    
    @property
    def token_url(self) -> str:
        """Get the token URL."""
        return f"{self.api_base_url}/oauth/token"
    
    def validate_credentials(self) -> bool:
        """Check if required credentials are configured."""
        return bool(self.client_id and self.client_secret)


def get_config() -> TrainingPeaksConfig:
    """Get the configuration instance."""
    return TrainingPeaksConfig()