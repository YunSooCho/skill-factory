# OnepageCRM API Integration

## Overview
Implementation of OnepageCRM API for simple CRM management for Yoom automation.

## Supported Features
- ✅ Deal: Create, Get, Update, Search
- ✅ Contact: Create, Get, Update, Search
- ✅ Company: Get, Update, Search
- ✅ Note: Create
- ✅ Action: Create

## Setup

### Get API Credentials
Visit https://app.onepagecrm.com/settings/api to get user ID and API key.

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
```python
from onepagecrm_client import OnepageCRMClient, Contact, Deal

user_id = "your_user_id"
api_key = "your_api_key"

async with OnepageCRMClient(user_id=user_id, api_key=api_key) as client:
    pass
```

## Usage

```python
# Create contact
contact = Contact(
    first_name="John",
    last_name="Doe",
    email="john@example.com"
)
await client.create_contact(contact)

# Create deal
deal = Deal(name="Software License", value=50000.0)
await client.create_deal(deal)
```

## Notes
- Async operations with rate limiting
- Simple and lightweight CRM
- Full pipeline support