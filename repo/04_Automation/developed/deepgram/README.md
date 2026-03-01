# Deepgram API Client

Production-ready API client for deepgram with full error handling and rate limiting.

## Features

✅ **Full Error Handling** - Comprehensive error handling with detailed messages
✅ **Rate Limiting** - Built-in rate limiting to prevent API throttling
✅ **Async/Await** - Modern async/await support with aiohttp
✅ **Type Hints** - Full type annotations for better IDE support
✅ **Retry Logic** - Automatic retry with exponential backoff
✅ **Logging** - Configurable request/response logging

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import asyncio
from deepgram_client import DeepgramClient

async def main():
    # Initialize with your API key
    async with DeepgramClient(api_key="your_api_key") as client:
        result = await client.list_items()
        print(result.data)

asyncio.run(main())
```

## API Methods

