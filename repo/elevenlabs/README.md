# ElevenLabs API Integration

## Overview
Implementation of ElevenLabs AI voice synthesis API for Yoom automation.

## Supported Features

### API Actions (8 operations)
- ✅ Text to Speech (basic)
- ✅ Text to Speech with Timestamps
- ✅ Text to Speech with Sound Effects
- ✅ Voice Conversion
- ✅ Create Dubbing
- ✅ Get Dubbing
- ✅ Get Dubbed File
- ✅ Audio Noise Removal
- ✅ Add Pronunciation Dictionary

### Triggers
- No triggers supported

## Setup

### 1. Get API Credentials
1. Visit https://elevenlabs.io/ and sign up
2. Go to Profile > API Key
3. Generate a new API Key
4. Copy your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from elevenlabs_client import ElevenLabsClient

async def main():
    api_key = "your_api_key"

    async with ElevenLabsClient(api_key=api_key) as client:
        # Get voices
        voices = await client.get_voices()
        if voices:
            audio = await client.text_to_speech(
                text="Hello world!",
                voice_id=voices[0].voice_id
            )
            print(f"Generated audio")
```

### Voice Management
```python
# Get all available voices
voices = await client.get_voices()

for voice in voices:
    print(f"{voice.name} ({voice.language})")
    if voice.gender:
        print(f"  Gender: {voice.gender}")
```

### Text to Speech
```python
# Basic TTS
audio = await client.text_to_speech(
    text="This is a sample text to be converted to speech.",
    voice_id="21m00Tcm4TlvDq8ikWAM",
    model_id="eleven_multilingual_v2"
)

# TTS with custom voice settings
audio = await client.text_to_speech(
    text="Custom voice settings example.",
    voice_id="voice_id",
    voice_settings={
        "stability": 0.75,
        "similarity_boost": 0.6,
        "style": 0.5
    }
)
```

### Text to Speech with Timestamps
```python
# TTS with word-level timestamps
result = await client.text_to_speech_with_timestamps(
    text="Hello world, this is a test.",
    voice_id="voice_id"
)

# Access timestamps
for word in result.get("alignment", []):
    print(f"{word['char']}: {word['start']}s - {word['end']}s")
```

### Text to Speech with Sound Effects
```python
# TTS with sound effects
result = await client.text_to_speech_sound_effects(
    text="Thunder and lightning struck.",
    voice_id="voice_id",
    sound_effects=[
        {"type": "thunder", "intensity": 0.8},
        {"type": "lightning", "intensity": 0.6}
    ]
)
```

### Voice Conversion
```python
# Convert voice from audio to another voice
result = await client.convert_voice(
    source_audio_url="https://example.com/original.mp3",
    target_voice_id="21m00Tcm4TlvDq8ikWAM"
)

# Access converted audio URL
converted_audio_url = result.get("audio_url")
```

### Audio Dubbing
```python
# Create dubbing job
dubbing = await client.create_dubbing(
    source_url="https://example.com/video.mp4",
    target_lang="es",  # Spanish
    source_lang="en",  # English
    voice_id="voice_id"  # Optional
)

print(f"Dubbing ID: {dubbing.dubbing_id}")
print(f"Status: {dubbing.status}")

# Check dubbing status
import asyncio
while True:
    result = await client.get_dubbing(dubbing.dubbing_id)
    status = result.get("status")

    if status == "completed":
        print("Dubbing complete!")
        break
    elif status == "failed":
        print("Dubbing failed")
        break

    await asyncio.sleep(5)

# Get dubbed file URL
download_url = await client.get_dubbing_file(dubbing.dubbing_id)
print(f"Download from: {download_url}")
```

### Audio Enhancement
```python
# Remove noise from audio
result = await client.audio_noise_removal(
    audio_url="https://example.com/noisy-audio.mp3"
)

enhanced_url = result.get("audio_url")
```

### Pronunciation Dictionary
```python
# Add pronunciation dictionary
pron_dict = await client.add_pronunciation_dictionary(
    name="Technical Terms",
    voice_id="voice_id",
    rules=[
        {"from": "AI", "to": "ay-eye"},
        {"from": "API", "to": "ay-pee-eye"},
        {"from": "GIF", "to": "jif"}
    ]
)
print(f"Created dictionary: {pron_dict.name}")

# Get dictionary details
pron_dict = await client.get_pronunciation_dictionary(
    dictionary_id=pron_dict.dictionary_id
)
print(f"Rules: {pron_dict.rules_count}")

# Delete dictionary
await client.delete_pronunciation_dictionary(pron_dict.dictionary_id)
```

## Integration Type
- **Type:** API Key (Header-based)
- **Authentication:** `xi-api-key` header
- **Protocol:** HTTPS REST API v1

## Testability
- ✅ All API actions testable with valid credentials
- ❌ No webhook triggers available

## Voice Models

Available models:
- `eleven_multilingual_v2` - Recommended, supports 29 languages
- `eleven_monolingual_v1` - English only, faster
- `eleven_turbo_v2` - Lower latency

```python
audio = await client.text_to_speech(
    text="Hello world",
    voice_id="voice_id",
    model_id="eleven_turbo_v2"  # For faster generation
)
```

## Voice Settings

Fine-tune voice output:
```python
voice_settings = {
    "stability": 0.5,           # 0-1, higher = more stable
    "similarity_boost": 0.75,   # 0-1, higher = more similar to original
    "style": 0.5,               # 0-1, higher = more expressive (v2 only)
    "use_speaker_boost": True   # Improve clarity
}
```

## Language Codes

Common language codes for dubbing:
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

```python
dubbing = await client.create_dubbing(
    source_url="https://example.com/audio.mp3",
    target_lang="ja",  # Japanese
    source_lang="en"   # English
)
```

## Best Practices

### Caching Audio
```python
# Cache generated audio URLs to avoid regenerating
cache = {}

async def get_tts(text, voice_id):
    key = f"{voice_id}:{hash(text)}"
    if key in cache:
        return cache[key]

    audio = await client.text_to_speech(text, voice_id)
    cache[key] = audio
    return audio
```

### Batch Processing
```python
# Process multiple texts efficiently
texts = ["Hello", "World", "Test"]
tasks = [client.text_to_speech(t, voice_id) for t in texts]
results = await asyncio.gather(*tasks)
```

### Error Handling
```python
try:
    audio = await client.text_to_speech(
        text="Test",
        voice_id="voice_id"
    )
except Exception as e:
    print(f"TTS failed: {e}")
    # Handle gracefully
```

### Dubbing Polling
```python
async def wait_for_dubbing(dubbing_id, timeout=600):
    """Wait for dubbing to complete with timeout"""
    start = asyncio.get_event_loop().time()

    while True:
        if asyncio.get_event_loop().time() - start > timeout:
            raise TimeoutError("Dubbing timeout")

        result = await client.get_dubbing(dubbing_id)
        status = result.get("status")

        if status == "completed":
            return result
        elif status in ("failed", "cancelled"):
            raise Exception(f"Dubbing {status}")

        await asyncio.sleep(10)
```

## Notes

- Audio content is returned directly; for URLs, upload to cloud storage
- Free tier has character usage limits
- Premium voices require subscription
- Dubbing may take significant time for long content
- Implement proper rate limiting for production use