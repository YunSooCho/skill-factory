# Ecomail API Integration

## Overview
Implementation of Ecomail email marketing API for Yoom automation.

## Supported Features

### API Actions (9 operations)
- ✅ Subscriber: Create, Get detail, Get from list, Update, Delete, Search, Search contact
- ✅ Campaign: Get statistics
- ✅ Transactional Email: Get statistics

### Triggers (3 events)
- ✅ New Open
- ✅ New Click
- ✅ New Bounce

## Setup

### 1. Get API Credentials
1. Visit https://ecomailapp.cz/ and sign up
2. Go to Settings > Integrations > API
3. Get your API Key

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
from ecomail_client import EcomailClient

async def main():
    api_key = "your_api_key"
    list_id = "your_list_id"

    async with EcomailClient(api_key=api_key) as client:
        # Create subscriber
        subscriber = await client.create_subscriber(
            email="john@example.com",
            list_id=list_id
        )
        print(f"Subscriber: {subscriber.email}")
```

### Subscriber Management
```python
# Create subscriber with details
subscriber = await client.create_subscriber(
    email="jane@example.com",
    list_id=list_id,
    first_name="Jane",
    last_name="Doe",
    tags=["new-signup", "newsletter"],
    phone="+1234567890",
    gender="female"
)

# Get subscriber detail
subscriber = await client.get_subscriber_detail(subscriber.id)
print(f"Status: {subscriber.status}")

# Get subscriber from list
subscriber = await client.get_subscriber_from_list(
    list_id=list_id,
    subscriber_email="john@example.com"
)

# Update subscriber
imported = await client.update_subscriber(
    subscriber_id=subscriber.id,
    first_name="Janet",
    tags=["updated"]
)

# Delete subscriber
await client.delete_subscriber(subscriber.id)
```

### Search Operations
```python
# Search subscribers
subscribers = await client.search_subscribers(
    email="john@example.com",
    list_id=list_id,
    limit=50
)

# Search contacts by query
contacts = await client.search_contact("john")
```

### Campaign Statistics
```python
# Get campaign statistics
stats = await client.get_campaign_stats(campaign_id="123")

if stats:
    print(f"Campaign: {stats.name}")
    print(f"Sent: {stats.sent}")
    print(f"Opens: {stats.opens}")
    print(f"Clicks: {stats.clicks}")
    print(f"Bounces: {stats.bounces}")
```

### Transactional Email Statistics
```python
# Get all transactional stats
stats = await client.get_transactional_email_stats()
print(f"Total sent: {stats.total_sent}")
print(f"Delivered: {stats.delivered}")
print(f"Opens: {stats.opens}")

# Get stats for date range
stats = await client.get_transactional_email_stats(
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

## Integration Type
- **Type:** API Key (Header-based)
- **Authentication:** `key` header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Settings > Webhooks in Ecomail
2. Add your webhook endpoint URL
3. Select events to track:
   - `open` - Email opened
   - `click` - Link clicked
   - `bounce` - Email bounced
4. Ecomail will POST event data to your endpoint

Example webhook payload:
```json
{
  "event": "open",
  "data": {
    "subscriber": {
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

## List Management

### Finding Your List ID
```python
# You need to get your list ID from Ecomail dashboard
# Go to Lists and copy the list ID from the URL or list settings

# Example: https://ecomailapp.cz/lists/12345/edit
# List ID: 12345

list_id = "12345"
```

## Best Practices

### Subscriber Organization
```python
# Always use tags to categorize subscribers
await client.create_subscriber(
    email="user@example.com",
    list_id=list_id,
    tags=["newsletter", "customer"]
)
```

### Statistics Analysis
```python
# Analyze campaign performance regularly
stats = await client.get_campaign_stats(campaign_id)
open_rate = stats.opens / stats.sent * 100 if stats.sent > 0 else 0
click_rate = stats.clicks / stats.opens * 100 if stats.opens > 0 else 0

print(f"Open rate: {open_rate:.2f}%")
print(f"Click rate: {click_rate:.2f}%")
```

### Date Filtering
```python
# Use date ranges for better statistics
from datetime import datetime, timedelta

end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

stats = await client.get_transactional_email_stats(
    start_date=start_date,
    end_date=end_date
)
```