"""Models for the voice agent core."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PasswordResetResult(BaseModel):
    """Result of a password reset operation."""
    
    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    temporary_password: Optional[str] = Field(None, description="Generated temporary password")
    
    @classmethod
    def error_response(cls, message: str = "I'm sorry, I didn't get that. Please try again.") -> "PasswordResetResult":
        """Create a standard error response.
        
        Args:
            message: Custom error message
            
        Returns:
            PasswordResetResult with success=False and no password
        """
        return cls(
            success=False,
            message=message,
            temporary_password=None
        )


class VoiceContext(BaseModel):
    """Context information for voice agent processing."""
    
    session_id: str = Field(description="Unique identifier for the voice session")
    user_id: Optional[str] = Field(None, description="User identifier if available")
    audio_quality: float = Field(1.0, description="Audio quality score (0.0-1.0)", ge=0.0, le=1.0) 