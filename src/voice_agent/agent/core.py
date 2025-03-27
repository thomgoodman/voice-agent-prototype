"""Core agent implementation for voice-enabled password reset."""
import os
import json
import logging
from typing import List, Optional, Dict, Any

from openai import AsyncClient
from pydantic import BaseModel, Field

from .models import PasswordResetResult, VoiceContext
from .tools import PasswordResetTool


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("voice_agent")


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
        
        # Define tool schema for OpenAI function calling
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "reset_password",
                    "description": "Reset a user's password and generate a temporary password",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "Optional user identifier"
                            }
                        },
                        "required": []
                    }
                }
            }
        ]

        # Agent instructions
        self._system_prompt = """You are a helpful voice assistant that helps users reset their passwords.
        When a user requests a password reset, use the reset_password tool to generate a temporary password.
        
        Consider the following phrases as password reset requests:
        - "reset my password"
        - "forgot my password"
        - "can't login" or "can't log in"
        - "trouble logging in"
        - "having issues with my password"
        - "locked out of my account"
        - "need a new password"
        
        When you detect any request related to login problems or password issues, use the reset_password tool.
        Always assume login trouble is related to password issues unless explicitly stated otherwise.
        
        Provide clear, concise responses suitable for voice interaction."""

    async def run(self, user_input: str) -> PasswordResetResult:
        """Process a user request.
        
        Args:
            user_input: Text from user's voice input
            
        Returns:
            PasswordResetResult containing operation status and temporary password
        """
        try:
            if not user_input or not isinstance(user_input, str):
                logger.warning("Empty or invalid input received")
                return PasswordResetResult.error_response()

            logger.info(f"Processing user input: '{user_input}'")

            # Check if this is likely a password reset request
            password_keywords = ["password", "reset", "forgot", "credentials", "login", "can't log in", "locked out", "trouble logging in", "issues", "can't access", "need a new password"]
            if not any(kw in user_input.lower() for kw in password_keywords):
                logger.info("Input doesn't appear to be related to password reset")
                return PasswordResetResult.error_response(
                    "I'm sorry, I didn't understand that. I can help you reset your password if needed."
                )

            # Process with OpenAI
            response = await self._client.chat.completions.create(
                model=self.model,
                temperature=self._temperature,
                tools=self.tools,
                tool_choice="auto",  # Let the model decide if it needs to call the tool
                messages=[
                    {"role": "system", "content": self._system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )

            # Log the response
            logger.info(f"Model response: {response.model_dump_json(indent=2)}")
            
            message = response.choices[0].message
            
            # Check if the model decided to call the tool
            if message.tool_calls:
                logger.info(f"Tool calls detected: {len(message.tool_calls)}")
                
                for tool_call in message.tool_calls:
                    # Log tool call details
                    logger.info(f"Tool call ID: {tool_call.id}")
                    logger.info(f"Function: {tool_call.function.name}")
                    logger.info(f"Arguments: {tool_call.function.arguments}")
                    
                    if tool_call.function.name == "reset_password":
                        # Parse arguments
                        args = json.loads(tool_call.function.arguments)
                        user_id = args.get("user_id")
                        
                        # Call the password reset tool
                        logger.info(f"Executing password reset for user_id: {user_id}")
                        result = await self._reset_tool(user_id)
                        
                        # Log the result
                        logger.info(f"Password reset result: {result}")
                        return result
            
            # If the model didn't call the tool, but the input seems password-related,
            # check what the model said
            content = message.content or ""
            logger.info(f"No tool calls detected. Assistant response: {content}")
            
            # If the assistant is asking for clarification, pass that message to the user
            return PasswordResetResult.error_response(
                content or "I'm sorry, I couldn't process your password reset request. Please try again."
            )
            
        except Exception as e:
            # Handle all exceptions with a friendly error response
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return PasswordResetResult.error_response() 