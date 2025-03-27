"""Configuration management for the voice agent."""
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


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


# Global settings instance
settings = Settings() 