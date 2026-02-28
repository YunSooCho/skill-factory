# Dropcontact API Client

Complete API client for Dropcontact - email and contact enrichment service.

## Features

- Full API coverage for 2 endpoints
- Contact data enrichment
- Email finding and validation
- Result retrieval with polling
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from dropcontact_client import DropcontactClient

async def main():
    client = DropcontactClient(api_key="your_api_key")

    # Run enrichment
    enrichment = await client.run_enrichment({
        "name": "John Smith",
        "company": "Acme Corp",
        "domain": "acme.com"
    })

    # Get result
    result = await client.get_result(enrichment.enrichment_id)
    print(f"Email: {result.email}")

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Enrichment
- `run_enrichment()` - Start an enrichment job
- `get_result()` - Get enrichment results (poll for completion)

## Error Handling

All methods raise `DropcontactAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.