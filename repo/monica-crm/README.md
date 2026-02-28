# Monica CRM API Integration

## Overview
Implementation of Monica CRM API for personal relationship management for Yoom automation.

## Supported Features
- ✅ Create, Get, Update, Delete Contact
- ✅ Create Note, Get Notes
- ✅ Create Call
- ✅ Create Activity, Get Activities
- ✅ Create, Get, Update, Delete Deal
- ✅ Create Task, Get Tasks, Update Task, Complete Task
- ✅ Create Reminder, Get Reminders
- ✅ Create Tag
- ✅ Add/Remove Tag from Contact

## Setup

### Get API Token
Visit https://app.monicahq.com/settings/api and generate an API token.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from monica_crm_client import MonicaCRMClient, Contact, Note

domain = "your_domain"
api_token = "your_monica_api_token"

async with MonicaCRMClient(domain=domain, api_token=api_token) as client:
    pass
```

## Usage

```python
# Create contact
contact = Contact(
    first_name="John",
    last_name="Doe",
    company="Example Corp"
)
created = await client.create_contact(contact)

# Create note
note = Note(contact_id=contact.id, body="Meeting notes")
await client.create_note(note)

# Create deal
deal = Deal(company_id=contact.id, name="Deal name", amount=50000.0)
await client.create_deal(deal)
```

## Notes
- Async operations with built-in rate limiting
- Comprehensive CRM for personal relationships
- Full CRUD for all entities