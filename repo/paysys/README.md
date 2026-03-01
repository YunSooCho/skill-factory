# Paysys API Client

Python async client for Comprehensive payment processing system. Payment.

## Features

- Create Payment
- Get Payment
- Refund Payment
- List Payments
- Get Account Balance
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
from paysys_client import PaysysClient

async def main():
    api_key = "your_api_key_here"

    async with PaysysClient(api_key) as client:
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

1. Create Payment
2. Get Payment
3. Refund Payment
4. List Payments
5. Get Account Balance

## Authentication

API authentication using API key or OAuth token. Set your credentials when initializing the client:

```python
client = PaysysClient(api_key="your_api_key")
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

- Base URL: https://api.paysys.com
- Official API Documentation: Visit service provider's API documentation
- Rate Limits: Check service provider's documentation

## Requirements

See `requirements.txt` for dependencies.
