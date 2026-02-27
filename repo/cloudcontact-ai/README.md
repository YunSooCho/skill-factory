# CloudContact AI Contact Management Integration

## Overview
Implementation of CloudContact AI API for Yoom automation.

## Supported Features

### Contact Management (2 endpoints)
- ✅ Create Contact
- ✅ Search Contacts

### SMS Messaging (2 endpoints)
- ✅ Get Sent SMS Messages
- ✅ Sent SMS Messages by Campaign

### Campaign Management (1 endpoint)
- ✅ Get Campaigns (additional helper method)

## Setup

### 1. Get API Key
1. Visit [CloudContact AI](https://cloudcontact.ai/)
2. Sign up for an account
3. Go to Settings → API Keys
4. Generate your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Contact Management
```python
import asyncio
from cloudcontact_ai_client import CloudContactAIClient

async def contact_example():
    api_key = "your_api_key"

    async with CloudContactAIClient(api_key=api_key) as client:
        # Create a new contact
        contact = await client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="+15551234567",
            company="ACME Corporation",
            tags=["vip", "customer"],
            custom_fields={
                "account_number": "ACC-001",
                "notes": "Referral from existing customer"
            }
        )

        print(f"Contact ID: {contact.id}")
        print(f"Name: {contact.first_name} {contact.last_name}")
        print(f"Email: {contact.email}")
        print(f"Phone: {contact.phone}")

        # Create a minimal contact (only required field)
        contact = await client.create_contact(email="jane@example.com")
        print(f"Created contact with ID: {contact.id}")

        # Search contacts
        contacts = await client.search_contacts(
            email="john.doe@example.com"
        )

        print(f"Found contacts: {len(contacts)}")
        for c in contacts:
            print(f"- {c.first_name} {c.last_name} ({c.email})")

        # Search by phone
        contacts = await client.search_contacts(phone="+15551234567")

        # Search by name filter
        contacts = await client.search_contacts(
            first_name="John",
            company="ACME"
        )

        # Search by tags
        contacts = await client.search_contacts(tags=["vip"])
        print(f"VIP contacts: {len(contacts)}")

        # Paginated search
        contacts = await client.search_contacts(
            page=1,
            per_page=25
        )

        # Search with multiple filters
        contacts = await client.search_contacts(
            first_name="John",
            company="ACME Corporation",
            tags=["customer"]
        )

asyncio.run(contact_example())
```

### SMS Messaging
```python
import asyncio
from datetime import datetime, timedelta
from cloudcontact_ai_client import CloudContactAIClient

async def sms_example():
    api_key = "your_api_key"

    async with CloudContactAIClient(api_key=api_key) as client:
        # Get all sent SMS messages
        messages = await client.get_sent_sms_messages()

        print(f"Total sent messages: {len(messages)}")
        for msg in messages[:10]:  # First 10
            print(f"- {msg.phone}: {msg.message[:50]}...")
            print(f"  Status: {msg.status}")

        # Get sent messages filtered by phone number
        messages = await client.get_sent_sms_messages(phone="+15551234567")
        print(f"Messages to this phone: {len(messages)}")

        # Get sent messages by status
        messages = await client.get_sent_sms_messages(status="delivered")
        print(f"Delivered messages: {len(messages)}")

        # Get sent messages within date range
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()

        messages = await client.get_sent_sms_messages(
            start_date=start_date,
            end_date=end_date
        )
        print(f"Messages sent in last 7 days: {len(messages)}")

        # Get sent messages by campaign
        campaign_id = 12345
        messages = await client.get_sent_sms_by_campaign(campaign_id)

        print(f"Messages in campaign: {len(messages)}")
        for msg in messages:
            print(f"- {msg.phone}: {msg.status}")

        # Paginated results
        messages = await client.get_sent_sms_messages(
            page=1,
            per_page=50
        )

        # Combined filters
        messages = await client.get_sent_sms_messages(
            phone="+15551234567",
            status="delivered",
            start_date=start_date
        )

asyncio.run(sms_example())
```

### Campaign Management
```python
async def campaign_example():
    api_key = "your_api_key"

    async with CloudContactAIClient(api_key=api_key) as client:
        # Get all campaigns
        campaigns = await client.get_campaigns()

        print(f"Total campaigns: {len(campaigns)}")
        for campaign in campaigns:
            print(f"- {campaign.name} (Status: {campaign.status})")
            print(f"  Messages: {campaign.message_count}")

        # Filter campaigns by status
        campaigns = await client.get_campaigns(status="active")
        print(f"Active campaigns: {len(campaigns)}")

        # Get completed campaigns
        campaigns = await client.get_campaigns(status="completed")

        # Get messages for each active campaign
        campaigns = await client.get_campaigns(status="active")
        for campaign in campaigns:
            messages = await client.get_sent_sms_by_campaign(campaign.id)
            print(f"Campaign '{campaign.name}': {len(messages)} messages")

asyncio.run(campaign_example())
```

### Convenience Functions
```python
from cloudcontact_ai_client import create_contact_simple, search_contacts_simple

# Quick contact creation without context manager
contact = asyncio.run(create_contact_simple(
    api_key="your_api_key",
    email="quick@example.com",
    first_name="Quick",
    last_name="Search"
))

# Quick contact search
contacts = asyncio.run(search_contacts_simple(
    api_key="your_api_key",
    email="quick@example.com"
))

print(f"Found {len(contacts)} contacts")
```

## Integration Type
- **Type:** API Key (X-API-KEY header)
- **Authentication:** API key in custom header
- **Protocol:** HTTPS REST API
- **Response Format:** JSON

## API Response Objects

### Contact
```python
@dataclass
class Contact:
    id: int                              # Contact ID
    first_name: str                      # First name
    last_name: str                       # Last name
    email: str                           # Email address
    phone: str                           # Phone number
    company: str                         # Company name
    tags: List[str]                      # Associated tags
    custom_fields: Dict[str, Any]        # Custom field values
    created_at: datetime                 # Creation timestamp
    updated_at: datetime                 # Last update timestamp
    raw_response: Dict                   # Full API response
```

### SMSMessage
```python
@dataclass
class SMSMessage:
    id: int                              # Message ID
    phone: str                           # Recipient phone number
    message: str                         # Message content
    status: str                          # Message status (sent, delivered, failed)
    sent_at: datetime                    # Send timestamp
    campaign_id: int                     # Campaign ID
    campaign_name: str                   # Campaign name
    delivery_status: str                 # Delivery status
    raw_response: Dict                   # Full API response
```

### Campaign
```python
@dataclass
class Campaign:
    id: int                              # Campaign ID
    name: str                            # Campaign name
    status: str                          # Status (active, completed, cancelled)
    created_at: datetime                 # Creation timestamp
    message_count: int                   # Number of messages in campaign
    raw_response: Dict                   # Full API response
```

## Message Status

| Status | Description |
|--------|-------------|
| sent | Message successfully sent to carrier |
| delivered | Message delivered to recipient |
| failed | Message delivery failed |
| pending | Message is pending delivery |

## Campaign Status

| Status | Description |
|--------|-------------|
| active | Campaign is currently active |
| completed | Campaign has completed |
| cancelled | Campaign was cancelled |
| scheduled | Campaign is scheduled for future |

## Search Tips

1. **Exact vs Partial Match**:
   - Use `email` and `phone` for exact matches
   - Use `first_name`, `last_name`, and `company` for partial matches

2. **Tag Filtering**:
   - When providing `tags`, contacts must have ALL specified tags
   - Use `tags=["vip"]` for single tag
   - Use `tags=["vip", "customer"]` for multiple tags (AND logic)

3. **Pagination**:
   - Always check if more pages are available
   - Use `per_page` to control result count (max 100)
   - Start with `page=1` and increment

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters, resource not found, duplicate resources
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Resource not found
- **409 Conflict**: Contact already exists
- **429 Rate Limit**: Too many requests

## Testability
- ✅ All API actions are testable with valid API key
- ⚠️ SMS sending may require credits
- ⚠️ Rate limits apply based on your plan
- ✅ Contact operations are free to test

## Notes
- Contact creation requires at least one of: first_name, last_name, email, or phone
- Tags can be used to segment and organize contacts
- Custom fields allow storing additional information
- SMS messages can be filtered by recipient, status, and date range
- Campaigns help organize bulk messaging
- Search results are paginated - use page/per_page for navigation
- Email addresses are stored in lowercase
- Phone numbers should be in international format (with country code)
- API key must be kept secure and not exposed in client-side code