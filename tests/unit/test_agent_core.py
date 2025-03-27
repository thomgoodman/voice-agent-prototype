"""Unit tests for voice agent core."""
import os
import pytest
from typing import Optional
from pydantic import BaseModel
from unittest.mock import AsyncMock, MagicMock, patch

from voice_agent.agent.core import VoiceAgent
from voice_agent.agent.tools import PasswordResetTool
from voice_agent.agent.models import PasswordResetResult


class MockCompletions:
    """Mock completions API."""
    async def create(self, *args, **kwargs):
        return MagicMock(choices=[
            MagicMock(message=MagicMock(content="I'll help you reset your password"))
        ])


class MockChat:
    """Mock chat API."""
    def __init__(self):
        self.completions = MockCompletions()


class MockAsyncClient:
    """Mock OpenAI AsyncClient."""
    def __init__(self, api_key: Optional[str] = None):
        self.chat = MockChat()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "test-key")


@pytest.mark.asyncio
class TestVoiceAgent:
    """Test suite for VoiceAgent class."""

    @pytest.fixture
    async def agent(self):
        """Create a test agent instance."""
        mock_client = MockAsyncClient(api_key="test-key")
        return VoiceAgent(name="TestAgent", client=mock_client)

    async def test_agent_initialization(self, agent):
        """Test agent is properly initialized."""
        assert agent.name == "TestAgent"
        assert agent.model == "gpt-4-turbo"
        assert len(agent.tools) == 1

    async def test_agent_processes_reset_request(self, agent):
        """Test agent properly processes password reset request."""
        result = await agent.run("I need to reset my password")
        assert isinstance(result, PasswordResetResult)
        assert result.success is True
        assert result.temporary_password is not None

    async def test_agent_handles_invalid_request(self, agent):
        """Test agent properly handles invalid requests."""
        with pytest.raises(ValueError, match="Invalid request: Input cannot be empty"):
            await agent.run("")

    async def test_agent_tool_execution(self, agent):
        """Test agent properly executes password reset tool."""
        result = await agent.run("reset my password")
        assert isinstance(result, PasswordResetResult)
        assert result.success is True
        assert result.temporary_password is not None 