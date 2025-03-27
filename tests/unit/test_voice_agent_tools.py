import pytest
from datetime import datetime
from src.voice_agent.agent.tools import PasswordResetTool
from src.voice_agent.agent.models import PasswordResetResult

@pytest.fixture
def reset_tool():
    return PasswordResetTool(delay=0.3)

@pytest.mark.asyncio
async def test_reset_password_success(reset_tool):
    """Test successful password reset."""
    result = await reset_tool()  # No user_id required in new implementation
    assert isinstance(result, PasswordResetResult)
    assert result.success is True
    assert isinstance(result.temporary_password, str)
    assert len(result.temporary_password) >= 8
    assert "Password reset successful" in result.message

@pytest.mark.asyncio
async def test_reset_password_with_user_id(reset_tool):
    """Test password reset with optional user ID."""
    result = await reset_tool(user_id="test_user")
    assert isinstance(result, PasswordResetResult)
    assert result.success is True

@pytest.mark.asyncio
async def test_reset_password_simulated_delay(reset_tool):
    """Test that password reset has appropriate delay."""
    start_time = datetime.now()
    await reset_tool()
    duration = (datetime.now() - start_time).total_seconds()
    assert 0.2 <= duration <= 0.5  # Check delay is between 200-500ms

@pytest.mark.asyncio
async def test_reset_password_result_format(reset_tool):
    """Test that password reset result has correct format."""
    result = await reset_tool()
    assert hasattr(result, 'success')
    assert hasattr(result, 'message')
    assert hasattr(result, 'temporary_password')
    assert isinstance(result.success, bool)
    assert isinstance(result.message, str)
    assert isinstance(result.temporary_password, str) 