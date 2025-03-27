"""Models for the voice agent core."""
from typing import Optional
from pydantic import BaseModel, Field


class PasswordResetResult(BaseModel):
    """Result of a password reset operation."""
    success: bool = Field(description="Whether the password reset was successful")
    message: str = Field(description="Message describing the result")
    temporary_password: Optional[str] = Field(
        None, 
        description="Temporary password if reset was successful"
    )


class VoiceContext(BaseModel):
    """Context for voice agent operations."""
    session_id: str = Field(description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier if authenticated")
    audio_quality: float = Field(
        description="Quality score of the audio input",
        ge=0.0,
        le=1.0
    ) 