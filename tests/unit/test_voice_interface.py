import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import numpy as np
from voice_agent.voice.interface import VoiceInterface

@pytest.fixture
async def voice_interface():
    return VoiceInterface(
        sample_rate=16000,
        channels=1,
        chunk_size=1024,
        max_recording_seconds=5
    )

@pytest.mark.asyncio
async def test_voice_interface_initialization(voice_interface):
    """Test voice interface initialization with correct parameters."""
    assert voice_interface.sample_rate == 16000
    assert voice_interface.channels == 1
    assert voice_interface.chunk_size == 1024
    assert voice_interface.max_recording_seconds == 5
    assert voice_interface.format == 16  # Default format is 16-bit

@pytest.mark.asyncio
async def test_capture_audio(voice_interface):
    """Test capturing audio from microphone."""
    # Mock pyaudio components
    mock_pyaudio = MagicMock()
    mock_stream = MagicMock()
    
    # Setup stream to return a sequence of audio chunks
    # Calculate the number of chunks needed for 5 seconds of audio
    chunks_per_second = int(voice_interface.sample_rate / voice_interface.chunk_size)
    total_chunks = chunks_per_second * 5  # 5 seconds of recording
    
    # Create enough chunks to satisfy the loop in capture_audio
    chunks = [b'\x00\x00' * voice_interface.chunk_size] * total_chunks
    mock_stream.read.side_effect = chunks
    
    mock_pyaudio.open.return_value = mock_stream
    
    with patch('voice_agent.voice.interface.pyaudio.PyAudio', return_value=mock_pyaudio):
        audio_data = await voice_interface.capture_audio()
        
        # Check that audio data contains the mocked chunks
        assert len(audio_data) > 0
        assert mock_stream.read.call_count == total_chunks
        assert mock_stream.close.called
        assert mock_pyaudio.terminate.called

@pytest.mark.asyncio
async def test_play_audio(voice_interface):
    """Test playing audio through speakers."""
    # Create test audio data
    test_audio = b'\x00\x01' * 4096  # Simple sample audio data
    
    # Mock pyaudio components
    mock_pyaudio = MagicMock()
    mock_stream = MagicMock()
    mock_pyaudio.open.return_value = mock_stream
    
    with patch('voice_agent.voice.interface.pyaudio.PyAudio', return_value=mock_pyaudio):
        await voice_interface.play_audio(test_audio)
        
        # Check that pyaudio stream was set up correctly and used
        mock_pyaudio.open.assert_called_once()
        assert mock_stream.write.called
        assert mock_stream.close.called
        assert mock_pyaudio.terminate.called

@pytest.mark.asyncio
async def test_handle_empty_audio_for_playback(voice_interface):
    """Test handling of empty audio data during playback."""
    with pytest.raises(ValueError, match="Empty audio data"):
        await voice_interface.play_audio(b"") 