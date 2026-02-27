# Abyssale API Integration

## Overview
Implementation of Abyssale content generation API for Yoom automation.

## Supported Features
- ✅ Generate Content (banners, images, videos from templates)
- ✅ Get File (download generated content)
- ✅ List Templates
- ✅ Get Template Details
- ✅ Webhook Support (New Generation trigger)

## Setup

### 1. Get API Key
Visit https://www.abyssale.com/ and sign up for an account to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_abyssale_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from abyssale_client import AbyssaleClient

async def main():
    api_key = "your_key"

    async with AbyssaleClient(api_key=api_key) as client:
        # List templates
        templates = await client.list_templates()
        print(f"Found {len(templates)} templates")

        # Generate content
        generation = await client.generate_content(
            template_id=templates[0]["id"],
            format="jpg",
            elements={
                "title": "Hello",
                "subtitle": "World"
            }
        )
        print(f"Generated: {generation.url}")

asyncio.run(main())
```

### Download File
```python
async def download_example():
    async with AbyssaleClient(api_key="your_key") as client:
        generation_id = "generation_id_here"

        # Download to file
        content = await client.download_file(
            generation_id,
            output_path="output.jpg"
        )
        print(f"Downloaded {len(content)} bytes")
```

### Webhook Example
```python
def handle_webhook(request):
    import hashlib

    payload = request.body
    signature = request.headers.get("X-Webhook-Signature")

    # Verify signature
    if client.verify_webhook_signature(
        payload, signature, webhook_secret
    ):
        event = client.handle_webhook_event(request.json)
        print(f"Event: {event}")
```

## Integration Type
- **Type:** API Key
- **Authentication:** X-API-Key header
- **Protocol:** HTTPS REST API

## Testability
- ✅ Generate Content: Testable with valid API key and templates
- ✅ Get File: Testable after content generation
- ⚠️ Webhook: Requires public endpoint to test

## Notes
- Free plan may have generation limits
- Async generation requires webhook URL for callbacks
- Templates must be created in Abyssale dashboard first