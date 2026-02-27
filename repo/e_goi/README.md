# E-goi API Integration

## Overview
Implementation of E-goi multi-channel marketing automation API for Yoom automation.

## Supported Features

### API Actions (14 operations)
- ✅ Contact: Create, Get, Search, Update, Delete
- ✅ List: Create, List, Delete
- ✅ Tag: Create, List, Delete
- ✅ Campaign: List, Send to contact, Send to segment
- ✅ Segment: List

### Triggers (7 events)
- ✅ New Subscriber
- ✅ New Unsubscriber
- ✅ Opened Email
- ✅ Clicked Email
- ✅ Hard Bounced Email
- ✅ Soft Bounced Email
- ✅ Send Email

## Setup

### 1. Get API Credentials
1. Visit https://www.e-goi.com/ and sign up
2. Go to Settings > API
3. Generate a new API Token
4. Copy your API key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
```

## Usage

### Basic Example
```python
import asyncio
from e_goi_client import EGoiClient

async def main():
    api_key = "your_api_key"

    async with EGoiClient(api_key=api_key) as client:
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
# Create contact with list and tags
contact = await client.create_contact(
    email="jane@example.com",
    first_name="Jane",
    last_name="Doe",
    phone="+1234567890",
    list_id="list_123",
    tags=["new-signup", "newsletter"]
)

# Get contact
contact = await client.get_contact(contact.id)

# Search contacts
contacts = await client.search_contacts(
    query="john",
    list_id="list_123"
)

# Update multiple contacts
await client.update_contacts(
    contact_ids=["contact1", "contact2"],
    tags=["updated"]
)

# Delete contacts
await client.delete_contacts(["contact1", "contact2"])
```

### List Management
```python
# Create mailing list
mailing_list = await client.create_list(
    name="Newsletter Subscribers",
    description="Weekly newsletter recipients"
)

# Get all lists
lists = await client.get_lists()

# Delete list
await client.delete_list(list_id="list_123")
```

### Tag Management
```python
# Create tag
tag = await client.create_tag(name="vip-customer")

# List all tags
tags = await client.list_tags()

# Delete tag
await client.delete_tag(tag.id)
```

### Campaign Management
```python
# List all campaigns
campaigns = await client.campaign_list()

# Send campaign to specific contact
await client.send_email_to_contact(
    campaign_id="campaign_123",
    contact_id="contact_456"
)

# Send campaign to segment
await client.send_email_to_segment(
    campaign_id="campaign_123",
    segment_id="segment_789"
)
```

### Segment Management
```python
# List all segments
segments = await client.segment_list()

# List segments for specific list
segments = await client.segment_list(list_id="list_123")
```

## Integration Type
- **Type:** API Key (Header-based)
- **Authentication:** APIKey header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Settings > Webhooks in E-goi
2. Add your webhook endpoint URL
3. Select events to track:
   - `subscribe` - New subscriber added
   - `unsubscribe` - New unsubscribe
   - `email_open` - Email opened
   - `email_link` - Email link clicked
   - `bounce_hard` - Hard bounce
   - `bounce_soft` - Soft bounce
   - `send_email` - Email sent
4. E-goi will POST event data to your endpoint

Example webhook payload:
```json
{
  "event": "email_open",
  "data": {
    "contact": {
      "id": "123",
      "email": "john@example.com"
    },
    "campaign": {
      "id": "456",
      "name": "Newsletter"
    },
    "timestamp": "2024-02-27T10:00:00Z"
  }
}
```

## Best Practices

### Contact Organization
```python
# Always assign contacts to lists for better management
contact = await client.create_contact(
    email="user@example.com",
    list_id="newsletter_list"
)
```

### Bulk Operations
```python
# Update multiple contacts at once
contact_ids = [c.id for c in contacts]
await client.update_contacts(
    contact_ids=contact_ids,
    tags=["bulk-update"]
)
```

### Campaign Segmentation
```python
# Use segments for targeted campaigns
segments = await client.segment_list()
await client.send_email_to_segment(
    campaign_id=campaign.id,
    segment_id=segments[0].id
)
```