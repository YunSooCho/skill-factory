# Myphoner API Client

Python client library for Myphoner API - Lead management and tracking system.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

You need an API key from Myphoner. Initialize the client with your API key:

```python
from myphoner_client import MyphonerClient

client = MyphonerClient(api_key="your_api_key_here")
```

## Usage Examples

### Create a Lead

```python
result = client.create_lead(
    list_id="list_123",
    name="John Doe",
    phone="+1234567890",
    email="john@example.com",
    company="Acme Inc."
)
```

### Get Lead Details

```python
lead = client.get_lead(lead_id="lead_123")
```

### Update a Lead

```python
result = client.update_lead(
    lead_id="lead_123",
    name="Jane Doe",
    phone="+0987654321"
)
```

### Search Leads

```python
leads = client.search_leads(
    list_id="list_123",
    query="John",
    status="todo",
    limit=50
)
```

### Mark Lead as Winner

```python
result = client.mark_winner(
    lead_id="lead_123",
    notes="Successful sale!"
)
```

### Mark Lead for Callback

```python
from datetime import datetime, timedelta

callback_date = datetime.now() + timedelta(days=3)
result = client.mark_callback(
    lead_id="lead_123",
    callback_date=callback_date,
    notes="Follow up in 3 days"
)
```

### List Columns

```python
columns = client.list_columns(list_id="list_123")
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

- Create Lead
- Get Lead
- Update Lead
- Delete Lead
- Search Leads
- Mark Winner
- Mark Loser
- Mark Callback
- List Columns

## Triggers

- Lead Marked as Winner
- Lead Marked as Loser
- Lead Archived
- Lead Marked as Callback

## Error Handling

```python
from myphoner_client import MyphonerClient, MyphonerAPIError

try:
    lead = client.get_lead(lead_id="invalid_id")
except MyphonerAPIError as e:
    print(f"Error: {e}")
```

## Notes

- API implements rate limiting (1 second between requests)
- All API actions return a dictionary with 'status', 'data', and 'status_code'
- Webhook signature verification uses HMAC-SHA256