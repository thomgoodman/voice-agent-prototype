#!/usr/bin/env python3
"""Tool Call Logging Demo.

This script demonstrates the agent's tool call functionality with detailed logging:
1. Use direct text input to trigger the password reset tool
2. Process through agent with logging
3. Display detailed tool call information
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path to allow imports from src
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import all required components
from voice_agent.agent import VoiceAgent

# Configure root logger to show debug messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ToolCallsDemo:
    """Demonstrates agent tool call functionality with detailed logging."""

    def __init__(self):
        """Initialize the demo with required components."""
        # Check for API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in .env file.")
        
        # Initialize agent
        self.agent = VoiceAgent(
            name="PasswordResetAgent",
            model="gpt-4-turbo",
            temperature=0.7,
            api_key=self.api_key
        )
    
    async def run(self, text_input: str = "reset my password"):
        """Run the agent and show tool call information.
        
        Args:
            text_input: Text input to trigger the tool call
        """
        print("\n==== Tool Call Logging Demo ====")
        print(f"Using text input: '{text_input}'")
        print("Check the logs for detailed tool call information.")
        
        try:
            # Process through agent to trigger tool calls
            print("\nProcessing through agent...")
            result = await self.agent.run(text_input)
            
            # Display the results
            print("\n==== Result ====")
            print(f"Success: {result.success}")
            print(f"Message: {result.message}")
            print(f"Temporary password: {result.temporary_password}")
            
            print("\n==== Demo Complete ====")
            print("Check the logs above for detailed tool call information.")
            
        except ValueError as e:
            error_msg = str(e)
            print(f"\n==== Request Handling ====")
            
            if "Clarification needed" in error_msg:
                print("The agent needs more information:")
                print(f"  {error_msg}")
                print("\nTry being more specific about needing a password reset.")
            elif "Invalid request" in error_msg:
                print("The request was not recognized as a password reset request:")
                print(f"  {error_msg}")
                print("\nTry asking specifically about resetting your password.")
            else:
                print(f"Error: {error_msg}")
            
            print("\n==== Demo Complete ====")
            print("Check the logs above for more detailed information.")
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            raise


async def main():
    """Run the tool calls demo."""
    demo = ToolCallsDemo()
    
    # Allow custom input from command line
    text_input = sys.argv[1] if len(sys.argv) > 1 else "reset my password"
    
    await demo.run(text_input)


if __name__ == "__main__":
    asyncio.run(main()) 