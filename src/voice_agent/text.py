"""Text processing module for voice agent.

This module handles speech-to-text and text-to-speech conversions using OpenAI APIs.
"""
from typing import Optional
import io
import wave
import tempfile
import os

import openai
from openai import AsyncOpenAI


class TextProcessor:
    """Handles text processing operations including speech-to-text and text-to-speech."""

    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        voice: str = "alloy",
        speech_model: str = "tts-1",
    ):
        """Initialize the text processor.
        
        Args:
            api_key: OpenAI API key
            model: Whisper model to use for speech-to-text
            voice: Voice to use for text-to-speech
            speech_model: TTS model to use
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.voice = voice
        self.speech_model = speech_model

    async def speech_to_text(self, audio_data: bytes, sample_rate: int = 16000, 
                             channels: int = 1, sample_width: int = 2) -> str:
        """Convert speech to text using Whisper API.
        
        Args:
            audio_data: Raw audio bytes to convert
            sample_rate: Audio sampling rate in Hz
            channels: Number of audio channels
            sample_width: Sample width in bytes (2 for 16-bit)
            
        Returns:
            Transcribed text
            
        Raises:
            ValueError: If audio_data is empty
        """
        if not audio_data:
            raise ValueError("Empty audio data")

        # Create a temporary WAV file with proper headers
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
            
            # Create WAV file with proper headers
            with wave.open(temp_path, 'wb') as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_data)
        
        try:
            # Open the file for sending to the API
            with open(temp_path, 'rb') as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="text"
                )
            return response
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using OpenAI TTS API.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Audio data as bytes
            
        Raises:
            ValueError: If text is empty
        """
        if not text:
            raise ValueError("Empty text input")

        response = await self.client.audio.speech.create(
            model=self.speech_model,
            voice=self.voice,
            input=text
        )
        
        return response.content