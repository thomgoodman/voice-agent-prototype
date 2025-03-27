import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from voice_agent.text import TextProcessor

@pytest.fixture
async def text_processor():
    return TextProcessor(api_key="test_key")

@pytest.mark.asyncio
async def test_speech_to_text_conversion(text_processor):
    """Test speech-to-text conversion using Whisper API."""
    test_audio = b"test_audio_data"
    
    # Mock the transcriptions.create method
    mock_transcription = AsyncMock()
    mock_transcription.return_value = "reset my password"
    
    # Set up the mock client structure
    with patch.object(text_processor, 'client') as mock_client:
        mock_client.audio.transcriptions.create = mock_transcription
        
        result = await text_processor.speech_to_text(test_audio)
        
        assert result == "reset my password"
        mock_transcription.assert_called_once()

@pytest.mark.asyncio
async def test_text_to_speech_conversion(text_processor):
    """Test text-to-speech conversion using OpenAI TTS API."""
    test_text = "Your password has been reset"
    
    # Create mock for audio.speech.create response
    mock_response = MagicMock()
    mock_response.content = b"synthesized_audio_data"
    
    # Create mock for the create method
    mock_create = AsyncMock()
    mock_create.return_value = mock_response
    
    # Set up the mock client structure
    with patch.object(text_processor, 'client') as mock_client:
        mock_client.audio.speech.create = mock_create
        
        result = await text_processor.text_to_speech(test_text)
        
        assert result == b"synthesized_audio_data"
        mock_create.assert_called_once_with(
            model=text_processor.speech_model,
            voice=text_processor.voice,
            input=test_text
        )

@pytest.mark.asyncio
async def test_speech_to_text_handles_empty_audio(text_processor):
    """Test handling of empty audio input."""
    with pytest.raises(ValueError, match="Empty audio data"):
        await text_processor.speech_to_text(b"")

@pytest.mark.asyncio
async def test_text_to_speech_handles_empty_text(text_processor):
    """Test handling of empty text input."""
    with pytest.raises(ValueError, match="Empty text input"):
        await text_processor.text_to_speech("")