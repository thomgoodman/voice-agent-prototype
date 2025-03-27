"""Tests for configuration management."""
import os
from pathlib import Path

import pytest
from pydantic import ValidationError
from pydantic_core import PydanticCustomError

from voice_agent.utils.config import Settings, get_settings


def test_settings_with_env_vars():
    """Test settings initialization with environment variables."""
    os.environ["OPENAI_API_KEY"] = "test-key"
    settings = get_settings()
    
    assert settings.openai_api_key == "test-key"
    assert settings.audio_sample_rate == 16000
    assert settings.model_name == "gpt-4-turbo-preview"
    assert isinstance(settings.app_dir, Path)


def test_settings_missing_required():
    """Test settings initialization with missing required values."""
    # Create a Settings instance with empty API key to test validation
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]
    
    # Test that Settings initialization raises ValidationError
    with pytest.raises(ValidationError):
        Settings(openai_api_key="") 