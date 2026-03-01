# Copper API Client

Complete API client for Copper CRM (formerly ProsperWorks) - a CRM for Google Workspace.

## Features

- Full API coverage for 12 endpoints
- Company management
- Person/contact management
- Task management
- Search capabilities
- Google Workspace integration
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from copper_client import CopperClient

async def main():
    client = CopperClient(api_key="your_api_key", email="your_email")

    # Create a company
    company = await client.create_company({
        "name": "Acme Corp",
        "website": "https://acme.com"
    })

    # Create a person
    person = await client.create_person({
        "name": "John Smith",
        "email": "john@example.com",
        "company_id": company.company_id
    })

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Companies
- `create_company()`, `update_company()`, `get_company()`, `search_companies()`

### People
- `create_person()`, `update_person()`, `get_person()`, `search_people()`

### Tasks
- `create_task()`, `update_task()`, `get_task()`, `search_tasks()`

## Error Handling

All methods raise `CopperAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.

## Webhooks

Supports 7 webhook triggers for new/updated companies, people, tasks, and opportunities.