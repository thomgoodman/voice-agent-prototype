#!/usr/bin/env python3
"""Text-only Voice Agent Demo.

This script demonstrates the agent workflow without audio recording:
1. Use direct text input instead of speech-to-text
2. Process through agent
3. Execute password reset tool
4. Convert response to speech
5. Save the audio response to a file instead of playing it
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
from voice_agent.text import TextProcessor
from voice_agent.agent import VoiceAgent


class TextDemoAgent:
    """Demonstrates agent workflow using direct text input."""

    def __init__(self):
        """Initialize the demo with required components."""
        # Check for API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in .env file.")
        
        # Initialize components
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
    
    async def run(self, text_input: str = "reset my password"):
        """Run the agent workflow with text input.
        
        Args:
            text_input: Text input simulating speech-to-text output
        """
        print("\n==== Voice Agent Password Reset Demo (Text Only) ====")
        print(f"Using text input: '{text_input}'")
        
        try:
            # Skip Step 1 (voice input) and Step 2 (speech-to-text)
            
            # Step 3 & 4: Process through agent with password reset tool
            print("\n1. Processing through agent...")
            result = await self.agent.run(text_input)
            
            # Format the response for TTS
            response_text = f"{result.message} Your temporary password is: {result.temporary_password}"
            print(f"\n2. Agent response: {response_text}")
            
            # Step 5: Convert response to speech
            print("\n3. Converting response to speech...")
            speech_data = await self.text_processor.text_to_speech(response_text)
            print(f"   Generated {len(speech_data)} bytes of audio")
            
            # Save the audio response to a file
            output_file = Path("./demo_output.mp3")
            output_file.write_bytes(speech_data)
            print(f"\n4. Saved audio response to {output_file.absolute()}")
            
            print("\n==== Demo Complete ====")
            print("Voice agent workflow executed successfully!")
            print(f"Temporary password: {result.temporary_password}")
            
        except Exception as e:
            print(f"\nError during demo: {str(e)}")
            raise


async def main():
    """Run the text-only demo."""
    demo = TextDemoAgent()
    
    # Allow custom input from command line
    text_input = sys.argv[1] if len(sys.argv) > 1 else "reset my password"
    
    await demo.run(text_input)


if __name__ == "__main__":
    asyncio.run(main()) 