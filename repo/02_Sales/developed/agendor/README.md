# Agendor API Client

Python client for Agendor CRM API.

## Features

- **Organizations**: Create, read, update, search organizations
- **People**: Create, read, update, search contacts
- **Deals**: Create, read, update, search deals/opportunities
- **Products**: Create, read, update, search products
- **Tasks**: Create, read, update, search tasks
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Rate Limiting**: Built-in rate limiter (10 requests/second)
- **Webhooks**: Webhook event handling for triggers

## Installation

```bash
pip install aiohttp
```

## API Actions (27)

1. Create Organization
2. Search Deal
3. Search Organization
4. Get Organization
5. Search Tasks of Person
6. Get Product
7. Update Deal
8. Create Task For Person
9. Update Deal Stage
10. Search Tasks of Deals
11. Update Product
12. Create Task For Organization
13. Create Person
14. Create Product
15. Update Organization
16. Create Task For Deal
17. Get Deal Of Person
18. Create Deal For Organization
19. Get Person
20. Update Person
21. Get Deal For Organization
22. Search Product
23. Search Tasks of Organization
24. Get Deal
25. Update Deal Status
26. Create Deal For Person
27. Search Person

## Triggers (13)

- Updated Stage Deal
- Created Organization
- Updated Deal
- Won Deal
- Updated Person
- Lost Deal
- Created Activity/Task/Comment
- Deleted Person
- Updated Organization
- Created Deal
- Deleted Organization
- Created Person
- Deleted Deal

## Usage

```python
import asyncio
from agendor import AgendorClient

async def main():
    # Initialize client with API token
    client = AgendorClient(api_token="your_api_token")

    # Create an organization
    org = await client.create_organization({
        "name": "Acme Corporation",
        "website": "https://acme.com",
        "annual_revenue": 1000000
    })
    print(f"Created org: {org.id} - {org.name}")

    # Create a person linked to organization
    person = await client.create_person({
        "name": "John Doe",
        "email": "john@acme.com",
        "phone": "+5511999999999",
        "organization_id": org.id
    })
    print(f"Created person: {person.id} - {person.name}")

    # Create a deal
    deal = await client.create_deal({
        "title": "New Project Contract",
        "value": 50000.0,
        "organization_id": org.id,
        "person_id": person.id
    })
    print(f"Created deal: {deal.id} - {deal.title}")

    # Update deal stage
    from agendor.agendor_client import DealStage
    deal = await client.update_deal_stage(deal.id, DealStage.PROPOSAL)
    print(f"Deal stage updated to: {deal.stage}")

    # Search organizations
    orgs = await client.search_organization(name="Acme")
    print(f"Found {len(orgs)} organizations")

    # Handle webhook
    webhook_data = {
        "event_type": "updated_stage_deal",
        "entity_type": "deal",
        "entity_id": deal.id
    }
    event = client.handle_webhook(webhook_data)
    print(f"Webhook event: {event['event_type']}")

asyncio.run(main())
```

## Testing

Requires API token (test organization/person/deal):
```python
# Create org
# Create person
# Create deal
# Update deal stage
# Search functions
```

## Authentication

Get API token from: https://app.agendor.com.br/api

## Error Handling

```python
from agendor.agendor_client import AgendorError

try:
    deal = await client.get_deal(deal_id)
except AgendorError as e:
    print(f"Error: {e.message} (HTTP {e.status_code})")
```

## Rate Limiting

Built-in rate limiter respects 10 requests/second limit.

## License

MIT