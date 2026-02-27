# Drip API Integration

## Overview
Implementation of Drip email marketing automation API for Yoom automation.

## Supported Features

### API Actions (12 operations)
- ✅ Subscriber: Create, Get, List, Update
- ✅ Workflow: Add to workflow, Remove from workflow
- ✅ Campaign: Subscribe, Unsubscribe, Get subscription, List subscribers
- ✅ Tags: Add tag, Remove tag
- ✅ Campaign List: List all campaigns, List all workflows
- ✅ Unsubscribe: Unsubscribe from all mailings

### Triggers (21 events)
- ✅ Removed Tag
- ✅ Subscriber Received Email
- ✅ Subscribed to Email Marketing
- ✅ Subscriber Marked as Undeliverable
- ✅ Subscriber Marked as Deliverable
- ✅ Updated Email Address
- ✅ Subscriber Created
- ✅ Subscriber Deleted
- ✅ Subscriber Became Lead
- ✅ Unsubscribed from Campaign
- ✅ Subscriber Visited Page
- ✅ Subscriber Bounced
- ✅ Completed Campaign
- ✅ Applied Tag
- ✅ Removed from Campaign
- ✅ Subscriber Complained
- ✅ Subscriber Clicked Email
- ✅ Unsubscribed All Mailings
- ✅ Subscribed to Campaign
- ✅ Subscriber Opened Email
- ✅ Subscriber Reactivated

## Setup

### 1. Get API Credentials
1. Visit https://www.getdrip.com/ and sign up
2. Go to Account Settings > API Integration
3. Generate a new API Token
4. Note your Account ID (found in account settings or API URL)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_token = "your_api_token"
account_id = "your_account_id"
```

## Usage

### Basic Example
```python
import asyncio
from drip_client import DripClient

async def main():
    api_token = "your_api_token"
    account_id = "123456789"

    async with DripClient(
        api_token=api_token,
        account_id=account_id
    ) as client:
        # Create subscriber
        subscriber = await client.create_subscriber(
            email="john@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"Subscriber: {subscriber.email}")
```

### Subscriber Management
```python
# Create subscriber with tags and custom fields
subscriber = await client.create_subscriber(
    email="jane@example.com",
    first_name="Jane",
    last_name="Doe",
    tags=["new-signup", "vip"],
    custom_fields={"source": "website"}
)

# Get subscriber
subscriber = await client.get_subscriber(subscriber.id)

# Update subscriber
await client.update_subscriber(
    subscriber_id=subscriber.id,
    first_name="Janet"
)

# Unsubscribe from all mailings
await client.unsubscribe_all(subscriber.id)
```

### Campaign Management
```python
# List campaigns
campaigns = await client.list_campaigns()

# Subscribe to campaign
await client.subscribe_to_campaign(
    subscriber_id=subscriber.id,
    campaign_id=campaigns[0].id
)

# Get campaign subscription
subscription = await client.get_campaign_subscription(
    campaign_id=campaigns[0].id,
    subscriber_id=subscriber.id
)

# List campaign subscribers
subscribers = await client.list_campaign_subscribers(campaigns[0].id)
```

### Workflow Automation
```python
# List workflows
workflows = await client.list_workflows()

# Add to workflow
await client.add_to_workflow(
    subscriber_id=subscriber.id,
    workflow_id=workflows[0].id
)

# Remove from workflow
await client.remove_from_workflow(
    subscriber_id=subscriber.id,
    workflow_id=workflows[0].id
)
```

### Tag Management
```python
# Add tag
await client.add_tag(subscriber.id, "vip-customer")

# Remove tag
await client.remove_tag(subscriber.id, "new-signup")
```

## Integration Type
- **Type:** API Token (Bearer)
- **Authentication:** Bearer token in Authorization header
- **Protocol:** HTTPS REST API
- **Rate Limiting:** Built-in rate limit handling (default: 3600 requests/hour)

## Testability
- ✅ All API actions testable with valid credentials
- ⚠️ Webhook triggers require public endpoint

## Webhook Setup

To receive triggers:
1. Go to Account Settings > Webhooks in Drip
2. Add your webhook endpoint URL
3. Select events to track
4. Drip will POST event data to your endpoint

Example webhook payload:
```json
{
  "event": "subscriber.created",
  "data": {
    "subscriber": {
      "id": "123456789",
      "email": "john@example.com",
      "status": "active"
    }
  },
  "occurred_at": "2024-02-27T10:00:00Z"
}
```

## Rate Limiting

The client automatically handles rate limiting:
- Monitors `X-RateLimit-Remaining` header
- Default: 3600 requests per hour
- Check `client._rate_limit_remaining` for current status