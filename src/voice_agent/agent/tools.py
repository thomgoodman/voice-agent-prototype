"""Tools for the voice agent."""
import asyncio
import secrets
import string
from typing import Optional

from openai import AsyncClient
from pydantic import BaseModel

from .models import PasswordResetResult


class PasswordResetTool:
    """Tool for handling password reset requests."""

    def __init__(self, delay: float = 0.3):
        """Initialize the password reset tool.
        
        Args:
            delay: Simulated processing delay in seconds
        """
        self._delay = delay

    async def __call__(self, user_id: Optional[str] = None) -> PasswordResetResult:
        """Execute password reset operation.
        
        Args:
            user_id: Optional user identifier
            
        Returns:
            PasswordResetResult with status and temporary password
        """
        # Simulate processing delay
        await asyncio.sleep(self._delay)
        
        # Generate temporary password
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        temp_password = ''.join(secrets.choice(chars) for _ in range(12))
        
        return PasswordResetResult(
            success=True,
            message="Password reset successful. Please use the temporary password to login.",
            temporary_password=temp_password
        ) 