import pytest
from src.voice_agent.agent.models import PasswordResetResult, VoiceContext

def test_password_reset_result_creation():
    """Test creation of PasswordResetResult model."""
    result = PasswordResetResult(
        success=True,
        message="Test message",
        temporary_password="TestPass123"
    )
    assert result.success is True
    assert result.message == "Test message"
    assert result.temporary_password == "TestPass123"
    
    # Test default values
    result = PasswordResetResult(
        success=False,
        message="Failed"
    )
    assert result.success is False
    assert result.temporary_password is None

def test_voice_context_creation():
    """Test creation of VoiceContext model."""
    context = VoiceContext(
        session_id="test-session",
        user_id="test-user",
        audio_quality=0.8
    )
    assert context.session_id == "test-session"
    assert context.user_id == "test-user"
    assert context.audio_quality == 0.8

def test_voice_context_validation():
    """Test validation of VoiceContext model."""
    with pytest.raises(ValueError):
        # Should fail because audio_quality > 1.0
        VoiceContext(
            session_id="test-session",
            audio_quality=1.5
        ) 