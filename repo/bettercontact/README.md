# Bettercontact API Client

Python client for Bettercontact contact enrichment API.

## Features

- Contact Enrichment: Enrich contact data with AI
- Get Results: Retrieve enrichment results

## Installation

```bash
pip install aiohttp
```

## API Actions (2)

1. Enrich Contact
2. Get Enrichment Results

## Usage

```python
import asyncio
from bettercontact import BettercontactClient

async def main():
    client = BettercontactClient(api_key="your_key")

    # Enrich contact
    result = await client.enrich_contact({
        "email": "john@acme.com",
        "name": "John Doe"
    })
    print(f"Enriched: {result.name}, Company: {result.company}")

    # Get result by ID
    result = await client.get_enrichment_result(result_id)
    print(f"Status: {result.status}")

asyncio.run(main())
```

## Testing

Requires API key for testing.

## License

MIT