#!/usr/bin/env python3
"""Voice Agent Demo.

This script demonstrates the full voice agent workflow:
1. Capture voice input
2. Convert speech to text
3. Process through agent
4. Execute password reset tool
5. Convert response to speech
6. Play audio response
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add the project root to Python path to allow imports from src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import all required components
from voice_agent.voice import VoiceInterface
from voice_agent.text import TextProcessor
from voice_agent.agent import VoiceAgent


class VoiceAgentDemo:
    """Integrates all voice agent components for demonstration."""

    def __init__(self):
        """Initialize the demo with all required components."""
        # Check for API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in .env file.")
        
        # Initialize components
        self.voice_interface = VoiceInterface(
            sample_rate=16000,
            channels=1,
            chunk_size=1024,
            max_recording_seconds=10
        )
        
        self.text_processor = TextProcessor(
            api_key=self.api_key,
            model="whisper-1",
            voice="alloy",
            speech_model="tts-1"
        )
        
        self.agent = VoiceAgent(
            name="PasswordResetAgent",
            model="gpt-4-turbo",
            temperature=0.7,
            api_key=self.api_key
        )
    
    async def run(self):
        """Run the complete voice agent workflow."""
        print("\n==== Voice Agent Password Reset Demo ====")
        print("Say 'reset my password' when recording begins...")
        time.sleep(1)  # Short pause before recording
        
        try:
            # Step 1: Capture voice input
            print("\n1. Capturing voice input...")
            audio_data = await self.voice_interface.capture_audio()
            print(f"   Captured {len(audio_data)} bytes of audio")
            
            # Step 2: Convert speech to text
            print("\n2. Converting speech to text...")
            text = await self.text_processor.speech_to_text(
                audio_data,
                sample_rate=self.voice_interface.sample_rate,
                channels=self.voice_interface.channels,
                sample_width=2  # 16-bit audio
            )
            print(f"   Recognized text: '{text}'")
            
            # Step 3 & 4: Process through agent with password reset tool
            print("\n3. Processing through agent...")
            result = await self.agent.run(text)
            
            # Format the response for TTS
            response_text = f"{result.message} Your temporary password is: {result.temporary_password}"
            print(f"\n4. Agent response: {response_text}")
            
            # Step 5: Convert response to speech
            print("\n5. Converting response to speech...")
            speech_data = await self.text_processor.text_to_speech(response_text)
            print(f"   Generated {len(speech_data)} bytes of audio")
            
            # Step 6: Play audio response
            print("\n6. Playing audio response...")
            await self.voice_interface.play_audio(speech_data)
            
            print("\n==== Demo Complete ====")
            print("Voice agent workflow executed successfully!")
            
        except Exception as e:
            print(f"\nError during demo: {str(e)}")
            raise


async def main():
    """Run the voice agent demo."""
    demo = VoiceAgentDemo()
    await demo.run()


if __name__ == "__main__":
    asyncio.run(main()) 