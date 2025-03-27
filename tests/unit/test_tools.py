import pytest
from datetime import datetime
from src.agent.tools import PasswordResetTool, ResetResult

@pytest.fixture
def reset_tool():
    return PasswordResetTool()

@pytest.mark.asyncio
async def test_reset_password_success(reset_tool):
    """Test successful password reset."""
    result = await reset_tool.reset_password(user_id="test_user")
    assert isinstance(result, ResetResult)
    assert result.success is True
    assert isinstance(result.temporary_password, str)
    assert len(result.temporary_password) >= 8
    assert result.message == "Password reset successful. Please use the temporary password to login."

@pytest.mark.asyncio
async def test_reset_password_invalid_user(reset_tool):
    """Test password reset with invalid user."""
    with pytest.raises(ValueError, match="Invalid user ID"):
        await reset_tool.reset_password(user_id="")

@pytest.mark.asyncio
async def test_reset_password_simulated_delay(reset_tool):
    """Test that password reset has appropriate delay."""
    start_time = datetime.now()
    await reset_tool.reset_password(user_id="test_user")
    duration = (datetime.now() - start_time).total_seconds()
    assert 0.2 <= duration <= 0.5  # Check delay is between 200-500ms

@pytest.mark.asyncio
async def test_reset_password_result_format(reset_tool):
    """Test that password reset result has correct format."""
    result = await reset_tool.reset_password(user_id="test_user")
    assert hasattr(result, 'success')
    assert hasattr(result, 'message')
    assert hasattr(result, 'temporary_password')
    assert isinstance(result.success, bool)
    assert isinstance(result.message, str)
    assert isinstance(result.temporary_password, str) 