# Bitrix API Client

Python client for Bitrix24 CRM API.

## Features

- Leads: Create, update, delete, search leads
- Deals: Full deal lifecycle management
- Contacts: Contact management
- Products: Product item management

## Installation

```bash
pip install aiohttp
```

## API Actions (20)

Full CRUD for leads, deals, contacts, product items

## Triggers (7)

- New Lead, Deal, Contact, Task
- Updated Lead, Deal, Contact

## Usage

```python
import asyncio
from bitrix import BitrixClient

async def main():
    # Initialize with webhook URL
    client = BitrixClient(webhook_url="https://your_domain.bitrix24.com/rest/user_id/code/")

    # Create lead
    lead = await client.create_lead({
        "TITLE": "New Lead",
        "NAME": "John",
        "LAST_NAME": "Doe"
    })
    print(f"Lead created: {lead.id}")

    # Create deal
    deal = await client.create_deal({
        "TITLE": "Big Deal",
        "OPPORTUNITY": 10000
    })
    print(f"Deal created: {deal.id}")

    # Search leads
    leads = await client.search_lead({"NAME": "John"})
    print(f"Found {len(leads)} leads")

asyncio.run(main())
```

## Authentication

1. Get webhook URL from Bitrix24
2. Format: https://your_domain.bitrix24.com/rest/user_id/webhook_code/

## License

MIT