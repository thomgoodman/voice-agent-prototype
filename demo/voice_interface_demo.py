#!/usr/bin/env python3
"""Voice Interface Demo.

This script demonstrates the basic audio recording and playback capabilities
of the voice agent's voice interface.
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add the project root to Python path to allow imports from src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from voice_agent.voice import VoiceInterface


async def run_demo():
    """Run the voice interface demonstration."""
    print("Voice Interface Demo")
    print("===================")
    print("\nThis demo will record audio from your microphone and play it back.")
    
    # Create the voice interface with shorter recording time
    voice_interface = VoiceInterface(
        sample_rate=16000,
        channels=1,
        chunk_size=1024,
        max_recording_seconds=5
    )
    
    print("\nStep 1: Recording Audio")
    print("---------------------")
    print("Speak into your microphone when recording begins...")
    time.sleep(1)  # Short pause before recording
    
    # Capture audio from microphone
    audio_data = await voice_interface.capture_audio()
    
    print(f"\nCapture complete! Recorded {len(audio_data)} bytes of audio.")
    
    print("\nStep 2: Playing Back Audio")
    print("------------------------")
    print("You should hear your own voice played back...")
    time.sleep(1)  # Short pause before playback
    
    # Play the recorded audio
    await voice_interface.play_audio(audio_data)
    
    print("\nDemo Complete!")
    print("==============")
    print("The voice interface is functioning correctly.")


if __name__ == "__main__":
    asyncio.run(run_demo()) 