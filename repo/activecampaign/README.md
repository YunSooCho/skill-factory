# ActiveCampaign API Integration

## Overview
Implementation of ActiveCampaign CRM and marketing automation API for Yoom automation.

## Supported Features

### API Actions (16 operations)
- ✅ Account: Create, Get, Update, Delete
- ✅ Contact: Create, Get, List, Search, Delete
- ✅ Contact-List: Add to list, Remove from list
- ✅ Contact-Account: Link contact to account
- ✅ Deal: Create
- ✅ Automation: Add contact to automation
- ✅ Notes: Add note
- ✅ Contact Score: Get score

### Triggers (4 events)
- ✅ Deal Created
- ✅ Contact Added
- ✅ Contact Created
- ✅ Contact Custom Field Value Created

## Setup

### 1. Get API Credentials
1. Visit https://activecampaign.com/ and sign up
2. Go to Settings > Developer
3. Get your API Key and API URL

Your API URL format: `https://YOUR_ACCOUNT.api-us1.com/api/3`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_url = "https://your-account.api-us1.com/api/3"
api_key = "your_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from activecampaign_client import ActiveCampaignClient

async def main():
    api_url = "https://your-account.api-us1.com/api/3"
    api_key = "your_key"

    async with ActiveCampaignClient(
        api_url=api_url,
        api_key=api_key
    ) as client:
        # Create contact
        contact = await client.create_contact(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Contact: {contact.email}")
```

### Contact Management
```python
# Create and search contacts
contact = await client.create_contact(
    email="jane@example.com",
    first_name="Jane",
    phone="+1234567890"
)

# Search contacts
contacts = await client.search_contacts(email="john@example.com")

# Get contact score
score = await client.get_contact_score(contact.id)
```

### Deal Management
```python
# Create a deal
deal = await client.create_deal(
    contact_id=contact.id,
    value=2500.00,
    currency="USD",
    stage="proposal"
)
print(f"Deal value: ${deal.value}")
```

### Account Management
```python
# Create account and link contact
account = await client.create_account(
    name="Example Corp",
    account_url="https://example.com"
)

await client.link_contact_account(contact.id, account.id)
```

### Notes
```python
await client.add_note(
    contact_id=contact.id,
    note="Follow-up call scheduled"
)
```

## Integration Type
- **Type:** API Key / OAuth
- **Authentication:** Api-Token header or Bearer token
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Settings > Webhooks in ActiveCampaign
2. Add your webhook endpoint URL
3. Select events to track
4. ActiveCampaign will POST event data to your endpoint

Example webhook events:
```json
{
  "type": "contact_added",
  "timestamp": "2024-02-27T10:00:00Z",
  "contact": {
    "id": "123",
    "email": "john@example.com"
  }
}
```