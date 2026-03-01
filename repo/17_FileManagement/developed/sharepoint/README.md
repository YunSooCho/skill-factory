# Sharepoint API Client

Python async client for Microsoft SharePoint document management platform. File Management.

## Features

- Upload File
- Download File
- Delete File
- List Files
- Get File Metadata
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
from sharepoint_client import SharepointClient

async def main():
    api_key = "your_api_key_here"

    async with SharepointClient(api_key) as client:
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

1. Upload File
2. Download File
3. Delete File
4. List Files
5. Get File Metadata

## Authentication

API authentication using API key or OAuth token. Set your credentials when initializing the client:

```python
client = SharepointClient(api_key="your_api_key")
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

- Base URL: https://graph.microsoft.com/v1.0/sites
- Official API Documentation: Visit service provider's API documentation
- Rate Limits: Check service provider's documentation

## Requirements

See `requirements.txt` for dependencies.
