# Nimble API Client

Python client library for Nimble API - CRM and contact management system.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

You need an API key from Nimble. Initialize the client with your API key:

```python
from nimble_client import NimbleClient

client = NimbleClient(api_key="your_api_key_here")
```

## Usage Examples

### Create a Contact

```python
result = client.create_contact(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="+1234567890",
    company="Acme Inc.",
    title="Sales Manager",
    tags=["customer", "priority"]
)
```

### Get Contact Details

```python
contact = client.get_contact(contact_id="contact_123")
```

### Update a Contact

```python
result = client.update_contact(
    contact_id="contact_123",
    title="Senior Sales Manager",
    tags=["customer", "priority", "VIP"]
)
```

### Search Contacts

```python
contacts = client.search_contact(
    query="John Doe",
    company="Acme",
    tags=["VIP"],
    limit=50
)
```

### Assign Tags to Contact

```python
result = client.assign_tag_to_contact(
    contact_id="contact_123",
    tags={"customer", "VIP", "new"}
)
```

### Create Contact Note

```python
result = client.create_contact_note(
    contact_id="contact_123",
    note="Meeting scheduled for next week",
    note_type="call"
)
```

### Create a Deal

```python
from datetime import datetime

result = client.create_deal(
    title="Enterprise Software Deal",
    value=50000.0,
    currency="USD",
    probability=75,
    expected_close_date="2024-03-31",
    contact_id="contact_123"
)
```

### Get Deal Details

```python
deal = client.get_deal(deal_id="deal_123")
```

### Update Deal

```python
result = client.update_deal(
    deal_id="deal_123",
    probability=90,
    status="negotiating"
)
```

### List Deals

```python
deals = client.list_deals(
    status="negotiating",
    limit=50
)
```

### Create Draft Message

```python
result = client.create_draft_message(
    contact_id="contact_123",
    subject="Follow-up Meeting",
    body="Hi, would like to schedule a follow-up...",
    message_type="email"
)
```

## Webhook Handling

```python
# Verify webhook signature
is_valid = client.verify_webhook_signature(
    payload=request_body,
    signature=request.headers.get("X-Webhook-Signature"),
    webhook_secret="your_webhook_secret"
)

# Handle webhook event
data = client.handle_webhook(payload)
```

## API Actions

### Contact Management
- Create Contact
- Get Contact
- Update Contact
- Delete Contact
- Search Contact
- Assign Tag to Contact
- Create Contact Note
- Update Contact Note
- Search Contact Notes

### Deal Management
- Create Deal
- Get Deal
- Update Deal
- Delete Deal
- List Deals

### Message Management
- Create Draft Message
- Search Draft Messages

## Triggers

- New Contact

## Error Handling

```python
from nimble_client import NimbleClient, NimbleAPIError

try:
    contact = client.get_contact(contact_id="invalid_id")
except NimbleAPIError as e:
    print(f"Error: {e}")
```

## Notes

- API uses Bearer token authentication
- Contact fields are structured with modifiers (personal, mobile, etc.)
- Webhook signature verification uses HMAC-SHA256
- All dates should be in ISO 8601 format