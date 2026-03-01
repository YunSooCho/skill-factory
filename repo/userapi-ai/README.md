# Userapi Ai API Client

Python async client for AI-powered user management and API service. Website Building.

## Features

- Create User
- Get User
- Update User
- Delete User
- List Users
- Authenticate User
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
from userapi_ai_client import UserapiAiClient

async def main():
    api_key = "your_api_key_here"

    async with UserapiAiClient(api_key) as client:
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

1. Create User
2. Get User
3. Update User
4. Delete User
5. List Users
6. Authenticate User

## Authentication

API authentication using API key or OAuth token. Set your credentials when initializing the client:

```python
client = UserapiAiClient(api_key="your_api_key")
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

- Base URL: https://api.userapi.ai
- Official API Documentation: Visit service provider's API documentation
- Rate Limits: Check service provider's documentation

## Requirements

See `requirements.txt` for dependencies.
