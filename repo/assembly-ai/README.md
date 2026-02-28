# Assembly AI API Client

Python async client for AssemblyAI speech-to-text API.

## Features

- Audio file upload
- Transcription with speaker diarization
- Key phrase detection
- Entity detection
- Sentiment analysis
- Summarization
- Polling for completion

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from assembly_ai_client import AssemblyAIClient

async def main():
    api_key = "your_key"

    async with AssemblyAIClient(api_key) as client:
        # Transcribe audio with speaker diarization
        transcript = await client.transcribe_audio(
            audio_url="https://example.com/audio.mp3",
            enable_speaker_diarization=True,
            speakers_expected=2,
            poll=True
        )

        print(f"Transcript: {transcript.text}")

asyncio.run(main())
```

## API Actions

1. Transcribe Audio
2. Upload Media File
3. Get Transcription Result

## Documentation

- [Assembly AI Documentation](https://www.assemblyai.com/docs/)