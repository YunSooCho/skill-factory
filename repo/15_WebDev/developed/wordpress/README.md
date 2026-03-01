# Wordpress API Client

Python async client for Content management system and website builder. Website Building.

## Features

- List Posts
- Get Post
- Create Post
- Update Post
- Delete Post
- List Pages
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
from wordpress_client import WordpressClient

async def main():
    api_key = "your_api_key_here"

    async with WordpressClient(api_key) as client:
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

1. List Posts
2. Get Post
3. Create Post
4. Update Post
5. Delete Post
6. List Pages

## Authentication

API authentication using API key or OAuth token. Set your credentials when initializing the client:

```python
client = WordpressClient(api_key="your_api_key")
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

- Base URL: https://api.wordpress.org
- Official API Documentation: Visit service provider's API documentation
- Rate Limits: Check service provider's documentation

## Requirements

See `requirements.txt` for dependencies.
