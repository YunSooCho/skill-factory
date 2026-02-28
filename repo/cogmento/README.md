# Cogmento API Client

Complete API client for Cogmento CRM system.

## Features

- Full API coverage for 20 endpoints
- Deal management with full CRUD
- Contact management
- Task management
- Product management
- Search and filtering capabilities
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from cogmento_client import CogmentoClient

async def main():
    client = CogmentoClient(api_key="your_api_key")

    # Create a deal
    deal = await client.create_deal({
        "name": "Enterprise Contract",
        "value": 100000.0,
        "stage": "Negotiation"
    })

    # List deals
    deals = await client.list_deals()

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Deals
- `create_deal()`, `update_deal()`, `get_deal()`, `list_deals()`

### Companies
- `create_company()`, `update_company()`, `get_company()`, `list_companies()`

### Contacts
- `create_contact()`, `update_contact()`, `get_contact()`, `list_contacts()`

### Tasks
- `create_task()`, `update_task()`, `get_task()`, `list_tasks()`

### Products
- `create_product()`, `update_product()`, `get_product()`, `list_products()`

## Error Handling

All methods raise `CogmentoAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.

## Webhooks

Supports 8 webhook triggers for new/updated deals, contacts, companies, and tasks.