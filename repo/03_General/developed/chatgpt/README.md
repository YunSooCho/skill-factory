# ChatGPT API Client

Python async client for OpenAI's ChatGPT API.

## Features

- ✅ Generate text with GPT models
- ✅ Text-to-speech conversion
- ✅ Speech-to-text transcription (Whisper)
- ✅ List available models
- ✅ Web search-augmented generation
- ✅ Create and manage conversation threads
- ✅ Image analysis (GPT-4 Vision)
- ✅ Advanced generation parameters
- ✅ Webhook support (Thread Message Created)
- ✅ Async/await support
- ✅ Type hints and dataclasses

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://platform.openai.com/api-keys

## Usage

### Initialize Client

```python
import asyncio
from chatgpt_client import ChatGPTAPIClient

async def main():
    api_key = "your-api-key-here"

    async with ChatGPTAPIClient(api_key) as client:
        # Use the client
        pass

asyncio.run(main())
```

### Generate Text

Simple text generation.

```python
async with ChatGPTAPIClient(api_key) as client:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]

    response = await client.generate_text(
        messages=messages,
        model="gpt-4",
        temperature=0.7,
        max_tokens=500
    )

    print(f"Response: {response.content}")
    print(f"Tokens used: {response.usage}")
```

### Generate Text with Web Search

Text generation with web browsing capability.

```python
async with ChatGPTAPIClient(api_key) as client:
    response = await client.generate_text_with_web_search(
        messages=[
            {"role": "user", "content": "What are the latest developments in AI?"}
        ],
        model="gpt-4o"  # Use models with browsing capability
    )

    print(f"Response: {response.content}")
```

### Generate Text with Advanced Settings

Fine-tune text generation with advanced parameters.

```python
async with ChatGPTAPIClient(api_key) as client:
    response = await client.generate_text_advanced(
        messages=messages,
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.5,
        presence_penalty=0.3,
        stop_sequences=["<END>", "STOP"],
        max_tokens=1000
    )

    print(response.content)
```

### Generate Text from Image

Analyze images with GPT-4 Vision.

```python
async with ChatGPTAPIClient(api_key) as client:
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ]

    response = await client.generate_text_with_image(
        messages=messages,
        model="gpt-4-vision-preview"
    )

    print(f"Image description: {response.content}")
```

### Generate Text from Image URL

Simpler method for image analysis.

```python
async with ChatGPTAPIClient(api_key) as client:
    response = await client.generate_text_from_image_url(
        image_url="https://example.com/image.jpg",
        prompt="What objects are in this image?",
        model="gpt-4-vision-preview"
    )

    print(response.content)
```

### List Models

Get list of available models.

```python
async with ChatGPTAPIClient(api_key) as client:
    models = await client.list_models()

    print(f"Available models: {len(models)}")
    for model in models:
        print(f"  - {model.id}")
```

### Create Thread

Create a conversation thread.

```python
async with ChatGPTAPIClient(api_key) as client:
    thread = await client.create_thread(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ],
        metadata={"user_id": "123", "topic": "general"}
    )

    print(f"Thread ID: {thread.id}")
    print(f"Created at: {thread.created_at}")
```

### Add Message to Thread

Add a message to an existing thread.

```python
async with ChatGPTAPIClient(api_key) as client:
    message = await client.add_message_to_thread(
        thread_id="thread-abc123",
        content="What's the weather like?",
        role="user"
    )

    print(f"Message ID: {message.id}")
    print(f"Status: {message.status}")
```

### Text to Speech

Convert text to audio.

```python
async with ChatGPTAPIClient(api_key) as client:
    response = await client.text_to_speech(
        text="Hello, this is a test of the text-to-speech API.",
        model="tts-1",
        voice="alloy",  # alloy, echo, fable, onyx, nova, shimmer
        output_format="mp3"
    )

    # Save audio file
    with open("output.mp3", "wb") as f:
        f.write(response.audio_data)

    print(f"Audio saved as {response.format}")
```

### Speech to Text

Transcribe audio file to text.

```python
async with ChatGPTAPIClient(api_key) as client:
    response = await client.speech_to_text(
        file_path="audio.mp3",
        model="whisper-1",
        language="en",  # Optional
        prompt="Transcribe the following audio"  # Optional
    )

    print(f"Transcription: {response.text}")
    print(f"Language: {response.language}")
    print(f"Duration: {response.duration}s")
```

### Webhook Handler

Handle webhooks for thread events.

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook/chatgpt")
async def chatgpt_webhook(request: Request):
    payload = await request.json()
    signature = request.headers.get("OpenAI-Signature", "")
    secret = "your-webhook-secret"

    # Verify signature
    if not client.verify_webhook(payload, signature, secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse event
    event = client.parse_webhook_event(payload)

    if event["event_type"] == "thread.message.created":
        print(f"New message in thread {event['thread_id']}")
        print(f"Content: {event['content']}")
        # Process new message

    return {"status": "ok"}
```

## API Actions

### Generate Text

Basic text generation.

**Parameters:**
- `messages` (List[Dict]): Message list with 'role' and 'content'
- `model` (str): Model name (default: "gpt-4")
- `temperature` (float): Sampling temperature (0.0-2.0)
- `max_tokens` (Optional[int]): Max tokens to generate
- `stream` (bool): Enable streaming

**Returns:** `ChatGenerationResponse`

### Generate Text with Web Search

Generation with web browsing.

**Parameters:**
- `messages` (List[Dict]): Message list
- `model` (str): Model with browsing (default: "gpt-4o")
- `temperature` (float): Sampling temperature
- `max_tokens` (Optional[int]): Max tokens

**Returns:** `ChatGenerationResponse`

### Generate Text Advanced

Generation with advanced parameters.

**Parameters:**
- `messages` (List[Dict]): Message list
- `model` (str): Model name
- `temperature` (float): Sampling temperature
- `max_tokens` (Optional[int]): Max tokens
- `top_p` (float): Nucleus sampling (0.0-1.0)
- `frequency_penalty` (float): Frequency penalty (-2.0 to 2.0)
- `presence_penalty` (float): Presence penalty (-2.0 to 2.0)
- `stop_sequences` (Optional[List[str]]): Stop sequences

**Returns:** `ChatGenerationResponse`

### Generate Text with Image

Analyze images.

**Parameters:**
- `messages` (List[Dict]): Messages with image content
- `model` (str): Vision model (default: "gpt-4-vision-preview")
- `max_tokens` (int): Max tokens (default: 500)

**Returns:** `ChatGenerationResponse`

### Generate Text from Image URL

Simpler image analysis.

**Parameters:**
- `image_url` (str): Image URL
- `prompt` (str): Analysis prompt
- `model` (str): Vision model
- `max_tokens` (int): Max tokens

**Returns:** `ChatGenerationResponse`

### List Models

List available models.

**Returns:** `List[Model]`

### Create Thread

Create conversation thread.

**Parameters:**
- `messages` (Optional[List[Dict]]): Initial messages
- `metadata` (Optional[Dict]): Thread metadata

**Returns:** `Thread`

### Add Message to Thread

Add message to thread.

**Parameters:**
- `thread_id` (str): Thread ID
- `content` (str): Message content
- `role` (str): Message role (default: "user")

**Returns:** `ThreadMessage`

### Text to Speech

Convert text to audio.

**Parameters:**
- `text` (str): Text to convert
- `model` (str): TTS model ('tts-1', 'tts-1-hd')
- `voice` (str): Voice ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')
- `output_format` (str): Format ('mp3', 'opus', 'aac', 'flac', 'wav', 'pcm')

**Returns:** `SpeechResponse`

### Speech to Text

Transcribe audio to text.

**Parameters:**
- `file_path` (str): Audio file path
- `model` (str): Whisper model ('whisper-1')
- `language` (Optional[str]): Language code
- `prompt` (Optional[str]): Transcription prompt

**Returns:** `TranscriptionResponse`

## Available Models

### Chat Models
| Model | Description | Context |
|-------|-------------|---------|
| gpt-4 | Most capable model | 8K/32K |
| gpt-4-turbo | Faster GPT-4 | 128K |
| gpt-4o | Multimodal, fast | 128K |
| gpt-3.5-turbo | Fast, cost-effective | 16K |

### Vision Models
| Model | Description |
|-------|-------------|
| gpt-4-vision-preview | GPT-4 with vision |
| gpt-4-turbo-vision-preview | Faster vision |

### Audio Models
| Model | Type | Description |
|-------|------|-------------|
| tts-1 | TTS | Standard quality |
| tts-1-hd | TTS | High quality |
| whisper-1 | STT | Speech recognition |

### Voices (TTS)
- `alloy` - Neutral, versatile
- `echo` - Male
- `fable` - British male
- `onyx` - Male, deep
- `nova` - Female
- `shimmer` - Female

## Webhook Events

### Thread Message Created

Triggered when a message is added to a thread.

**Event Type:** `thread.message.created`

**Payload:**
```json
{
  "type": "thread.message.created",
  "id": "evt-123",
  "timestamp": "2026-02-28T12:00:00Z",
  "data": {
    "thread_id": "thread-abc123",
    "message_id": "msg-xyz789",
    "content": "...",
    "role": "user"
  }
}
```

## Best Practices

1. **Temperature control:**
   - 0.0-0.3: Precise, consistent outputs
   - 0.4-0.7: Balanced (default)
   - 0.8-1.0: Creative, varied outputs

2. **Max tokens:** Set appropriate limits based on use case

3. **Streaming:** Enable for long responses to improve user experience

4. **Thread management:** Use threads for multi-turn conversations

5. **Error handling:** Always check for errors in responses

6. **Rate limits:** Monitor and implement backoff if needed

## API Reference

Official documentation: https://platform.openai.com/docs/api-reference

## Pricing

Check pricing at: https://platform.openai.com/pricing

## Support

For issues, visit: https://help.openai.com/