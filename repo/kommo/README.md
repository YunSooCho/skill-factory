# Kommo CRM API Integration

## Overview
Implementation of Kommo CRM API for Yoom automation.

## Supported Features
- ✅ Update Note
- ✅ Add Note
- ✅ Search Tags
- ✅ Search Notes by Entity Type
- ✅ Add Task
- ✅ Search Contacts
- ✅ Add Lead
- ✅ Update Contact
- ✅ Update Company
- ✅ Search Tasks
- ✅ Search Leads
- ✅ Add Contact
- ✅ Update Task
- ✅ Update Lead
- ✅ Add Company
- ✅ Search Companies
- ✅ Add Tags to Entity
- ✅ Search Notes by Entity ID

## Setup

### 1. Get API Credentials
Visit https://www.kommo.com/developers/ to:
1. Create an account or log in
2. Navigate to account settings
3. Generate an API key or set up OAuth 2.0

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
from kommo_client import KommoClient, Lead, Contact, Task

subdomain = "your_subdomain"
api_key = "your_kommo_api_key"

async with KommoClient(subdomain=subdomain, api_key=api_key) as client:
    # Use the client
    pass
```

## Usage

### Create Lead and Contact
```python
import asyncio
from kommo_client import KommoClient, Lead, Contact

async def main():
    subdomain = "your_subdomain"
    api_key = "your_kommo_api_key"

    async with KommoClient(subdomain=subdomain, api_key=api_key) as client:
        # Create lead
        lead = Lead(
            name="New Deal",
            status_id=123,
            pipeline_id=1,
            price=50000.0,
            responsible_user_id=1
        )
        created_lead = await client.add_lead(lead)

        # Create contact
        contact = Contact(
            name="John Doe",
            first_name="John",
            last_name="Doe",
            responsible_user_id=1
        )
        created_contact = await client.add_contact(contact)

asyncio.run(main())
```

### Tasks and Notes
```python
# Create a task
import time
task = Task(
    text="Follow up call",
    task_type_id=1,
    entity_type="leads",
    entity_id=lead_id,
    complete_till=int(time.time()) + 86400
)
created_task = await client.add_task(task)

# Add a note
note = Note(
    note_type="common",
    entity_type="leads",
    entity_id=lead_id,
    text="Initial meeting scheduled"
)
created_note = await client.add_note(note)
```

### Company
```python
from kommo_client import Company

# Create company
company = Company(
    name="Example Corp",
    responsible_user_id=1
)
created_company = await client.add_company(company)
```

### Search
```python
# Search leads
leads = await client.search_leads(query="deal")

# Search contacts
contacts = await client.search_contacts(query="John")

# Search tasks
tasks = await client.search_tasks(entity_type="leads", entity_id=lead_id)
```

### Tags
```python
# Search tags
tags = await client.search_tags(entity_type="leads")

# Add tags to entity
await client.add_tags_to_entity(
    entity_type="leads",
    entity_id=lead_id,
    tags=[tag_id_1, tag_id_2]
)
```

## Integration Type
- **Type:** API Key or OAuth 2.0 (Bearer token)
- **Authentication:** Bearer token via Authorization header
- **Protocol:** HTTPS REST API
- **Rate Limiting:** Built-in with 0.5s delay between requests
- **Retries:** Up to 3 retries with exponential backoff

## Error Handling
- **401 Unauthorized:** Invalid API key
- **403 Forbidden:** Insufficient permissions
- **404 Not Found:** Resource doesn't exist
- **429 Rate Limited:** Automatic retry
- **5xx Server Errors:** Automatic retry

## Data Models

### Lead
- `id`: Unique identifier (integer)
- `name`: Lead name
- `status_id`: Status identifier
- `pipeline_id`: Pipeline identifier
- `price`: Deal value
- `responsible_user_id`: Responsible user ID
- `created_by`: Creator user ID
- `custom_fields`: Custom fields list

### Contact
- `id`: Unique identifier
- `name`: Full name
- `first_name`: First name
- `last_name`: Last name
- `responsible_user_id`: Responsible user ID
- `created_by`: Creator user ID
- `custom_fields`: Custom fields list

### Company
- `id`: Unique identifier
- `name`: Company name
- `responsible_user_id`: Responsible user ID
- `created_by`: Creator user ID
- `custom_fields`: Custom fields list

### Task
- `id`: Unique identifier
- `text`: Task description
- `task_type_id`: Task type ID
- `entity_type`: Entity type (leads, contacts, companies)
- `entity_id`: Associated entity ID
- `complete_till`: Completion timestamp (Unix timestamp)
- `is_completed`: Completion status
- `responsible_user_id`: Assigned user ID

### Note
- `id`: Unique identifier
- `note_type`: Note type (common, call, email, etc.)
- `entity_type`: Entity type
- `entity_id`: Associated entity ID
- `text`: Note content
- `created_by`: Creator user ID
- `params`: Additional parameters

## Notes
- All operations are async
- Built-in rate limiting
- Automatic retry logic
- Complete CRUD for leads, contacts, companies, tasks, notes
- Tag management support

## API Documentation
Official Kommo API documentation: https://www.kommo.com/developers/