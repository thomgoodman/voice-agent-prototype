"""Core agent implementation for voice-enabled password reset."""
import os
from typing import List, Optional

from openai import AsyncClient
from pydantic import BaseModel, Field

from .models import PasswordResetResult, VoiceContext
from .tools import PasswordResetTool


class VoiceAgent:
    """Agent for handling voice-based password reset requests."""

    def __init__(
        self,
        name: str,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7,
        api_key: Optional[str] = None,
        client: Optional[AsyncClient] = None
    ):
        """Initialize the voice agent.
        
        Args:
            name: Name of the agent
            model: OpenAI model to use
            temperature: Sampling temperature
            api_key: OpenAI API key (defaults to env var)
            client: Optional pre-configured AsyncClient for testing
        """
        self.name = name
        self.model = model
        self._temperature = temperature
        self._client = client or AsyncClient(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self._reset_tool = PasswordResetTool()
        self.tools = [self._reset_tool]

        # Agent instructions
        self._system_prompt = """You are a helpful voice assistant that helps users reset their passwords.
        When a user requests a password reset, use the password reset tool to generate a temporary password.
        Always verify the request is about password reset before proceeding.
        Provide clear, concise responses suitable for voice interaction."""

    async def run(self, user_input: str) -> PasswordResetResult:
        """Process a user request.
        
        Args:
            user_input: Text from user's voice input
            
        Returns:
            PasswordResetResult containing operation status and temporary password
            
        Raises:
            ValueError: If the input is invalid or not a password reset request
        """
        if not user_input or not isinstance(user_input, str):
            raise ValueError("Invalid request: Input cannot be empty")

        # Process with OpenAI
        response = await self._client.chat.completions.create(
            model=self.model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        # Execute password reset if the request is valid
        # For MVP, we'll just check for keywords in the input
        if "reset" in user_input.lower() and "password" in user_input.lower():
            result = await self._reset_tool()
            return result
        
        raise ValueError("Invalid request: Must be a password reset request") 