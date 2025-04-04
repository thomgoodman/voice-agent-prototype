"""Voice interface module for handling audio input and output.

This module provides functionality for capturing audio from a microphone
and playing audio through speakers using PyAudio.
"""
import asyncio
from typing import Optional

import pyaudio


class VoiceInterface:
    """Handles voice input and output operations using PyAudio."""

    # PyAudio format constants
    PYAUDIO_FORMAT_MAP = {
        8: pyaudio.paInt8,
        16: pyaudio.paInt16,
        24: pyaudio.paInt24,
        32: pyaudio.paInt32,
        -32: pyaudio.paFloat32
    }

    def __init__(
        self, 
        sample_rate: int = 16000, 
        channels: int = 1, 
        chunk_size: int = 1024,
        max_recording_seconds: int = 30,
        format_bits: int = 16,
    ):
        """Initialize the voice interface.
        
        Args:
            sample_rate: Audio sampling rate in Hz
            channels: Number of audio channels (1 for mono, 2 for stereo)
            chunk_size: Number of frames per buffer
            max_recording_seconds: Maximum recording duration in seconds
            format_bits: Audio bit depth (8, 16, 24, 32 for int, -32 for float32)
            
        Raises:
            ValueError: If format_bits is not supported
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.max_recording_seconds = max_recording_seconds
        
        if format_bits not in self.PYAUDIO_FORMAT_MAP:
            supported = ", ".join(map(str, self.PYAUDIO_FORMAT_MAP.keys()))
            raise ValueError(f"Unsupported format: {format_bits}. Supported formats: {supported}")
        
        self.format = format_bits
        self.pyaudio_format = self.PYAUDIO_FORMAT_MAP[format_bits]
        
        # Calculated values
        self.max_chunks = int(self.sample_rate / self.chunk_size * self.max_recording_seconds)

    async def capture_audio(self) -> bytes:
        """Capture audio from microphone.
        
        This method captures audio from the default microphone until silence is detected
        or the maximum recording time is reached.
        
        Returns:
            Raw audio data as bytes
            
        Raises:
            RuntimeError: If audio capture fails
        """
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=self.pyaudio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            print("Recording... Speak now. (5 seconds)")
            
            # Initialize buffer to store recorded audio chunks
            frames = []
            
            # Calculate chunks per second
            chunks_per_second = int(self.sample_rate / self.chunk_size)
            
            # Record for 5 seconds (increased from the previous ~2 seconds)
            # This gives users more time to speak
            recording_seconds = 5
            total_chunks = chunks_per_second * recording_seconds
            
            for i in range(total_chunks):
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
                
                # Print countdown at each second
                if i % chunks_per_second == 0 and i > 0:
                    seconds_left = recording_seconds - (i // chunks_per_second)
                    if seconds_left > 0:
                        print(f"{seconds_left} seconds left...")
                
                # Small pause to allow for cooperative multitasking in async context
                if i % 5 == 0:
                    await asyncio.sleep(0.001)
            
            print("Recording complete.")
            
            # Combine all audio frames into a single byte string
            audio_data = b''.join(frames)
            return audio_data
            
        except Exception as e:
            raise RuntimeError(f"Failed to capture audio: {str(e)}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate()
    
    async def play_audio(self, audio_data: bytes) -> None:
        """Play audio through speakers.
        
        Args:
            audio_data: Raw audio bytes to play
            
        Raises:
            ValueError: If audio_data is empty
            RuntimeError: If audio playback fails
        """
        if not audio_data:
            raise ValueError("Empty audio data")
            
        try:
            # Check if this looks like WAV data with a header
            if audio_data.startswith(b'RIFF') and b'WAVE' in audio_data[0:12]:
                # If it's a WAV file, parse the header to get format information
                import wave
                import io
                
                wav_file = wave.open(io.BytesIO(audio_data), 'rb')
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                sample_rate = wav_file.getframerate()
                
                # Get just the audio data without the header
                wav_file.rewind()
                # Skip the header bytes
                frame_count = wav_file.getnframes()
                audio_data = wav_file.readframes(frame_count)
                
                # Update format to match the WAV file
                if sample_width == 1:
                    pyaudio_format = pyaudio.paInt8
                elif sample_width == 2:
                    pyaudio_format = pyaudio.paInt16
                elif sample_width == 3:
                    pyaudio_format = pyaudio.paInt24
                elif sample_width == 4:
                    pyaudio_format = pyaudio.paInt32
                else:
                    pyaudio_format = self.pyaudio_format
            else:
                # If not WAV data, use our default format
                channels = self.channels
                sample_rate = self.sample_rate
                pyaudio_format = self.pyaudio_format
        except Exception as e:
            # If we can't parse as WAV, fall back to default format
            print(f"Warning: Could not parse audio format, using default: {str(e)}")
            channels = self.channels
            sample_rate = self.sample_rate
            pyaudio_format = self.pyaudio_format
        
        p = pyaudio.PyAudio()
        
        try:
            stream = p.open(
                format=pyaudio_format,
                channels=channels,
                rate=sample_rate,
                output=True
            )
            
            print("Playing audio response...")
            
            # For larger audio data, we'll play it in chunks to be more responsive
            # and allow cooperative multitasking in async context
            chunk_size = self.chunk_size * 4  # Larger playback chunks for efficiency
            
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                stream.write(chunk)
                
                # Small pause to allow for cooperative multitasking
                if i % (chunk_size * 5) == 0:
                    await asyncio.sleep(0.001)
            
            print("Playback complete.")
            
        except Exception as e:
            raise RuntimeError(f"Failed to play audio: {str(e)}")
        finally:
            if 'stream' in locals():
                stream.stop_stream()
                stream.close()
            p.terminate() 