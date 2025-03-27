# Voice Agent

A voice-enabled password reset agent using OpenAI's APIs.

## Setup

1. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a virtual environment:
```bash
uv venv
```

3. Install dependencies:
```bash
uv pip install -e .
uv pip install python-dotenv
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Running the Demos

The project includes three demos that demonstrate the voice agent's functionality:

### 1. Voice Interface Demo

This is the simplest demo that tests just the audio recording and playback functionality without any AI processing.

```bash
uv run demo/voice_interface_demo.py
```

This will:
1. Record audio from your microphone for a few seconds
2. Play it back immediately through your speakers
3. Confirm that the voice interface is working correctly

This demo is useful for testing your microphone and speaker setup before running the full voice agent.

### 2. Text-Only Demo

This demo shows the complete agent workflow without requiring audio recording. It's perfect for quick testing and demonstration.

```bash
uv run demo/text_demo.py
```

This will:
1. Process the default input "reset my password"
2. Call the OpenAI LLM to analyze the request
3. Generate a temporary password
4. Convert the response to speech using OpenAI's TTS
5. Save the audio response to `demo_output.mp3`

You can also provide your own input text:

```bash
uv run demo/text_demo.py "I need to reset my password please"
```

### 3. Full Voice Agent Demo

This demo demonstrates the complete voice agent workflow with audio recording and playback.

```bash
uv run demo/voice_agent_demo.py
```

This will:
1. Record audio from your microphone
2. Convert speech to text using OpenAI's Whisper API
3. Process the text through the agent
4. Generate a temporary password
5. Convert the response to speech
6. Play the audio response through your speakers

**Note:** This demo requires a working microphone and speakers.

## Development

- Run tests: `uv run -m pytest`
- Format code: `uv run -m black src/ tests/ demo/`
- Check types: `uv run -m mypy src/`

## Project Structure

```
voice-agent/
├── src/
│   └── voice_agent/     # Main package
│       ├── agent/       # Agent core and tools
│       ├── voice/       # Voice interface components
│       ├── utils/       # Utility functions
│       ├── text.py      # Text processing (STT/TTS)
│       └── __init__.py
├── tests/               # Test suite
├── demo/                # Demo scripts
│   ├── voice_interface_demo.py  # Simple audio recording/playback demo
│   ├── text_demo.py             # Text-only agent demo
│   └── voice_agent_demo.py      # Full voice agent demo
├── docs/                # Documentation
│   ├── architecture.md  # System architecture diagram
├── config/              # Configuration files
├── .env                 # Environment variables (not in git)
├── pyproject.toml       # Project metadata and dependencies
├── uv.lock              # Lock file for reproducible installs
└── README.md            # This file
```

## Documentation

See the [docs](./docs) directory for detailed documentation, including:
- [System Architecture](./docs/architecture.md) - Component diagram and descriptions

## License

MIT 