# Contactship AI API Client

Complete API client for Contactship AI - AI-powered contact management with phone call capabilities.

## Features

- Full API coverage for 7 endpoints
- Contact management (CRUD operations)
- AI phone call automation
- Agent listing and management
- Search capabilities
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from contactship_ai_client import ContactshipAIClient

async def main():
    client = ContactshipAIClient(api_key="your_api_key")

    # Create a contact
    contact = await client.create_contact({
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "555-1234"
    })

    # Make an AI phone call
    result = await client.ai_phone_call({
        "contact_id": contact.contact_id,
        "script": "Business introduction",
        "agent_id": "agent_123"
    })

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Contacts
- `create_contact()`, `update_contact()`, `get_contact()`, `delete_contact()`, `search_contact()`

### AI Phone Calls
- `ai_phone_call()`

### Agents
- `list_agents()`

## Error Handling

All methods raise `ContactshipAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.