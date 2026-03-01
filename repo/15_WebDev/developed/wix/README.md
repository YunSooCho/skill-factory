# Wix API Client

Python async client for Cloud-based website development platform. Website Building.

## Features

- List Sites
- Get Site
- Create Page
- Update Page
- Delete Page
- Async/await support with aiohttp
- Automatic retries and error handling
- Rate limiting support
- Type hints
- Full API coverage

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from wix_client import WixClient

async def main():
    api_key = "your_api_key_here"

    async with WixClient(api_key) as client:
        # List items
        result = await client.list_items(limit=10)
        print(result.data)

        # Create item
        new_item = await client.create_item({"name": "Example", "value": 123})
        print(new_item.data)

        # Get specific item
        item = await client.get_item("item_id_here")
        print(item.data)

asyncio.run(main())
```

## API Actions

1. List Sites
2. Get Site
3. Create Page
4. Update Page
5. Delete Page

## Authentication

API authentication using API key or OAuth token. Set your credentials when initializing the client:

```python
client = WixClient(api_key="your_api_key")
```

## Error Handling

All API calls return a response object with success status, data, and optional error:

```python
result = await client.get_item("item_id")

if result.success:
    print(result.data)
else:
    print(f"Error: {result.error}, Status: {result.status_code}")
```

## Documentation

- Base URL: https://www.wixapis.com
- Official API Documentation: Visit service provider's API documentation
- Rate Limits: Check service provider's documentation

## Requirements

See `requirements.txt` for dependencies.
