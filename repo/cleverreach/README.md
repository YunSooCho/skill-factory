# CleverReach Email Marketing Integration

## Overview
Implementation of CleverReach Email Marketing API for Yoom automation.

## Supported Features

### Receiver Management (5 endpoints)
- ✅ Add Receiver
- ✅ Get Receiver Information
- ✅ Update Receiver
- ✅ Delete Receivers (single and batch)
- ✅ Search Receivers

### Event Management (1 endpoint)
- ✅ Add Event to Receiver

### Blacklist Management (1 endpoint)
- ✅ Register Email to Group Blacklist

### Webhook Triggers (1 trigger)
- ✅ New Receiver (webhook event parsing)

## Setup

### 1. Get API Key
1. Visit [CleverReach](https://www.cleverreach.com/)
2. Sign up for a free account
3. Get your API key from Account Settings → API
4. Note: You need your Group ID as well

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Add a New Receiver
```python
import asyncio
from cleverreach_client import CleverReachClient

async def add_example():
    api_key = "your_api_key"
    group_id = 12345

    async with CleverReachClient(api_key=api_key) as client:
        receiver = await client.add_receiver(
            group_id=group_id,
            email="john@example.com",
            source="signup_form",
            activated=True,
            attributes={
                "first_name": "John",
                "last_name": "Doe",
                "company": "ACME Corp"
            },
            global_attributes={
                "tags": ["vip", "customer"]
            }
        )

        print(f"Receiver ID: {receiver.id}")
        print(f"Email: {receiver.email}")
        print(f"Activated: {receiver.activated}")

asyncio.run(add_example())
```

### Get Receiver Information
```python
async def get_example():
    api_key = "your_api_key"
    group_id = 12345
    receiver_id = 67890

    async with CleverReachClient(api_key=api_key) as client:
        receiver = await client.get_receiver(receiver_id, group_id)

        print(f"Email: {receiver.email}")
        print(f"Source: {receiver.source}")
        print(f"Registered: {receiver.registered}")
        print(f"Attributes: {receiver.attributes}")

asyncio.run(get_example())
```

### Update Receiver
```python
async def update_example():
    api_key = "your_api_key"
    group_id = 12345
    receiver_id = 67890

    async with CleverReachClient(api_key=api_key) as client:
        receiver = await client.update_receiver(
            receiver_id=receiver_id,
            group_id=group_id,
            attributes={
                "first_name": "Jane",
                "last_name": "Doe Updated"
            }
        )

        print("Receiver updated successfully")

asyncio.run(update_example())
```

### Delete Receivers
```python
async def delete_example():
    api_key = "your_api_key"
    group_id = 12345

    async with CleverReachClient(api_key=api_key) as client:
        # Delete single receiver
        success = await client.delete_receiver(receiver_id=67890, group_id=group_id)
        print(f"Deleted: {success}")

        # Delete multiple receivers
        deleted_count = await client.delete_receivers(
            group_id=group_id,
            receiver_ids=[111, 222, 333]
        )
        print(f"Deleted count: {deleted_count}")

        # Delete by emails
        deleted_count = await client.delete_receivers(
            group_id=group_id,
            emails=["test@example.com", "user@example.com"]
        )
        print(f"Deleted count: {deleted_count}")

asyncio.run(delete_example())
```

### Search Receivers
```python
async def search_example():
    api_key = "your_api_key"
    group_id = 12345

    async with CleverReachClient(api_key=api_key) as client:
        # Get all receivers in group
        receivers = await client.search_receivers(group_id=group_id)

        print(f"Total receivers: {len(receivers)}")
        for receiver in receivers[:10]:  # First 10
            print(f"- {receiver.email}")

        # Search by email (partial match)
        receivers = await client.search_receivers(
            group_id=group_id,
            email="john@example.com"
        )

        # Paginated search
        receivers = await client.search_receivers(
            group_id=group_id,
            page=0,
            pagesize=25,
            order="desc",
            orderby="id"
        )

asyncio.run(search_example())
```

### Add Event to Receiver
```python
async def event_example():
    api_key = "your_api_key"
    group_id = 12345
    receiver_id = 67890

    async with CleverReachClient(api_key=api_key) as client:
        # Add purchase event
        success = await client.add_event_to_receiver(
            receiver_id=receiver_id,
            group_id=group_id,
            event_type="purchase",
            event_data={
                "amount": 99.99,
                "product": "Premium Plan",
                "currency": "USD"
            }
        )
        print(f"Event added: {success}")

        # Add click event
        success = await client.add_event_to_receiver(
            receiver_id=receiver_id,
            group_id=group_id,
            event_type="click",
            event_data={
                "link": "https://example.com/special-offer",
                "campaign": "Spring Sale"
            }
        )

asyncio.run(event_example())
```

### Blacklist Email
```python
async def blacklist_example():
    api_key = "your_api_key"

    async with CleverReachClient(api_key=api_key) as client:
        # Add to global blacklist
        success = await client.register_email_to_blacklist(
            email="spam@example.com",
            reason="User requested removal"
        )
        print(f"Blacklisted globally: {success}")

        # Add to group-specific blacklist
        success = await client.register_email_to_blacklist(
            email="unsubscribed@example.com",
            group_id=12345,
            reason="Unsubscribed from campaign"
        )
        print(f"Blacklisted in group: {success}")

asyncio.run(blacklist_example())
```

## Webhook Trigger: New Receiver

CleverReach can send webhooks when a new receiver is added. Here's how to handle it:

```python
from cleverreach_client import parse_webhook_event
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/cleverreach', methods=['POST'])
def handle_webhook():
    """Handle CleverReach webhook events"""
    payload = request.get_json()

    # Parse the webhook event
    event = parse_webhook_event(payload)

    print(f"Event Type: {event.event_type}")
    print(f"Receiver ID: {event.receiver_id}")
    print(f"Group ID: {event.group_id}")
    print(f"Timestamp: {event.timestamp}")

    # Handle "new_receiver" event
    if event.event_type == "receiver_created":
        # Do something with the new receiver
        print(f"New receiver created: {event.receiver_id}")
        # Fetch receiver details
        # ...

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

### WebhookEvent Object
```python
@dataclass
class WebhookEvent:
    event_type: str                      # Type of event
    receiver_id: int                     # Receiver ID
    group_id: int                        # Group ID
    timestamp: datetime                  # Event timestamp
    payload: Dict[str, Any]              # Full webhook payload
```

## Integration Type
- **Type:** API Key (Basic Auth)
- **Authentication:** Basic Auth with API key as username
- **Protocol:** HTTPS REST API
- **Webhooks:** Supported via external webhook endpoint

## API Response Objects

### Receiver
```python
@dataclass
class Receiver:
    id: int                              # Receiver ID
    email: str                           # Email address
    source: str                          # Source of the receiver
    activated: bool                      # Activation status
    registered: datetime                 # Registration timestamp
    deactivated: bool                    # Deactivation status
    attributes: Dict[str, Any]           # Custom attributes
    global_attributes: Dict[str, Any]    # Global attributes
    events: List[str]                    # Event types
    raw_response: Dict                   # Full API response
```

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters, receiver/group not found, email already exists
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Receiver or group not found
- **409 Conflict**: Email already exists or already blacklisted
- **429 Rate Limit**: Too many requests

## Testability
- ✅ Free tier available (up to 300 email recipients)
- ✅ All API actions are testable with valid API key
- ⚠️ Rate limits apply based on your plan

## Notes
- You need both API key and Group ID for most operations
- Group ID can be found in your CleverReach dashboard
- Subscribers can have custom attributes for additional data
- Events can be used to track subscriber interactions
- Blacklist is group-specific or global depending on parameters
- Webhooks need to be configured in CleverReach dashboard
- API documentation: https://rest.cleverreach.com/doc/