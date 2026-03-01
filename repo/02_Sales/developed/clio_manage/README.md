# Clio Manage API Client

Complete API client for Clio Manage - a legal practice management system.

## Features

- Full API coverage for 19 endpoints
- Case/Matter management
- Contact management (People/Companies)
- Task management with templates
- Time and expense tracking
- Communication logging
- Calendar management
- Bill management
- User and company search
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from clio_manage_client import ClioManageClient

async def main():
    client = ClioManageClient(api_key="your_api_key")

    # Create a matter (case)
    matter = await client.create_matter({
        "name": "Client Smith - Divorce Case",
        "client_id": 123,
        "description": "Divorce proceedings"
    })

    # Create a time entry
    time_entry = await client.create_time_entry({
        "matter_id": matter.matter_id,
        "duration": 3600,  # seconds
        "date": "2024-01-15",
        "note": "Initial consultation"
    })

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Matters (Cases)
- `create_matter()`, `update_matter()`, `get_matter()`, `search_matters()`
- `create_matter_folder()`, `create_matter_note()`

### Contacts
- `create_person_contact()`, `update_person_contact()`
- `create_company_contact()`, `update_company_contact()`
- `search_persons_or_companies()`, `search_users()`

### Tasks
- `create_task()`, `update_task()`, `get_task()`
- `assign_task_template_list()`

### Time & Expenses
- `create_time_entry()`
- `create_expense_entry()`

### Other
- `create_communication()`, `create_calendar_entry()`, `search_bills()`

## Error Handling

All methods raise `ClioAPIError` on API errors:
```python
try:
    matter = await client.create_matter(data)
except ClioAPIError as e:
    print(f"API Error: {e}")
```

## Rate Limiting

The client includes automatic rate limiting:
```python
client = ClioManageClient(
    api_key="your_api_key",
    max_requests_per_minute=100
)
```

## Webhooks

Supports 11 webhook triggers:
- New/Updated Tasks
- New Communications
- New Bills
- New Activities
- New Calendar Entries
- New Documents
- New/Updated Matters
- New Contacts

See the official Clio API documentation for webhook setup.