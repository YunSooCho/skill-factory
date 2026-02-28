# Close API Client

Complete API client for Close - a CRM for inside sales teams.

## Features

- Full API coverage for 19 endpoints
- Lead management with status tracking
- Contact management
- Opportunity/Deal tracking
- Task management
- Activity logging (Email, Call)
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
from close_client import CloseClient

async def main():
    client = CloseClient(api_key="your_api_key")

    # Create a lead
    lead = await client.create_lead({
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "555-1234",
        "company": "Acme Corp"
    })

    # Create a task for the lead
    task = await client.create_task({
        "lead_id": lead.lead_id,
        "text": "Follow up call",
        "due_date": "2024-01-20"
    })

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Leads
- `create_lead()`, `update_lead()`, `get_lead()`, `delete_lead()`, `search_leads()`

### Contacts
- `create_contact()`, `update_contact()`, `get_contact()`, `delete_contact()`, `search_contacts()`

### Opportunities
- `create_opportunity()`, `update_opportunity()`, `get_opportunity()`

### Tasks
- `create_task()`, `update_task()`, `get_task()`, `delete_task()`

### Activities
- `create_email_activity()`, `create_call_activity()`

## Error Handling

All methods raise `CloseAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included:
```python
client = CloseClient(
    api_key="your_api_key",
    max_requests_per_minute=100
)
```

## Webhooks

Supports 13 webhook triggers including new leads, completed tasks, new opportunities, and more.