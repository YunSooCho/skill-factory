# Cloze API Client

Complete API client for Cloze - a smart inbox and contact management system.

## Features

- Full API coverage for 14 endpoints
- Company and Person management with automatic updates
- Project management
- Communication record tracking
- To-do creation
- Timeline content management
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
from cloze_client import ClozeClient

async def main():
    client = ClozeClient(api_key="your_api_key")

    # Create or update a person
    person = await client.create_or_update_person({
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "555-1234"
    })

    # Search people
    results = await client.search_people(query="John")

    await client.close()

asyncio.run(main())
```

## API Endpoints

### People & Companies
- `create_or_update_person()`, `create_or_update_company()`
- `get_person()`, `get_company()`
- `delete_person()`, `delete_company()`
- `search_people()`, `search_company()`

### Projects
- `get_project()`, `delete_project()`, `search_project()`

### Communications & Timeline
- `create_communication_record()`, `create_timeline_content()`

### Tasks
- `create_to_do()`

## Error Handling

All methods raise `ClozeAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.

## Webhooks

Supports 3 webhook triggers for updated people, companies, and projects.