# DeepSeek API Client

Python async client for DeepSeek's LLM API.

## Features

- ✅ Generate text using DeepSeek's state-of-the-art LLM
- ✅ Async/await support for efficient operations
- ✅ Type hints and dataclasses for structured responses
- ✅ Comprehensive error handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key

Get your API key from: https://platform.deepseek.com/

## Usage

```python
import asyncio
from deepseek_client import DeepSeekAPIClient

async def main():
    api_key = "your-api-key-here"

    async with DeepSeekAPIClient(api_key) as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]

        response = await client.generate_text(
            messages=messages,
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=500
        )

        print(f"Response: {response.content}")
        print(f"Tokens used: {response.usage}")

asyncio.run(main())
```

## API Actions

### Generate Text

Generate text using DeepSeek's LLM models.

**Parameters:**
- `messages` (List[Dict]): List of message objects with 'role' and 'content'
- `model` (str): Model name (default: "deepseek-chat")
- `temperature` (float): Sampling temperature (0.0-2.0, default: 0.7)
- `max_tokens` (Optional[int]): Maximum tokens to generate
- `stream` (bool): Enable streaming (default: False)

**Returns:** `TextGenerationResponse`

## API Reference

Official documentation: https://platform.deepseek.com/api-docs/

## Models

- `deepseek-chat`: General-purpose chat model
- `deepseek-coder`: Code generation model

## Rate Limits

Check your account dashboard for rate limit information.

## Support

For issues, visit: https://github.com/deepseek-ai