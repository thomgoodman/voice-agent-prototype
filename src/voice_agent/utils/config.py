"""Configuration management for the voice agent."""
import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import PydanticCustomError


class Settings(BaseSettings):
    """Voice agent configuration settings."""
    
    # OpenAI Configuration
    openai_api_key: str
    model_name: str = "gpt-4-turbo-preview"
    
    # Audio Configuration
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    audio_chunk_size: int = 1024
    max_recording_seconds: int = 30
    
    # Application Paths
    app_dir: Path = Path(__file__).parent.parent.parent.parent
    config_dir: Path = app_dir / "config"
    temp_dir: Path = app_dir / "temp"
    
    # Optional API Configuration
    api_timeout: float = 10.0
    max_retries: int = 3
    retry_delay: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    def model_post_init(self, __context):
        """Validate after initialization."""
        if not self.openai_api_key:
            raise PydanticCustomError(
                "missing_api_key",
                "OPENAI_API_KEY is required but not provided",
                {"field": "openai_api_key"}
            )


# Global settings instance - do not initialize at import time
# to allow for proper testing of validation errors
def get_settings():
    """Get settings instance with validation."""
    return Settings() 