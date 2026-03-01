# Sender API Client

Python client for Sender API - email marketing service.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SenderClient

client = SenderClient(api_key="your-api-key")
```

## API Actions

### Add Subscriber

```python
result = client.add_subscriber(
    email="john@example.com",
    name="John Doe",
    fields={"phone": "+1234567890", "country": "US"}
)
```

### List Subscribers

```python
result = client.list_subscribers(limit=50, offset=0)
for subscriber in result['subscribers']:
    print(subscriber['email'])
```

### Get Subscriber

```python
subscriber = client.get_subscriber("john@example.com")
print(subscriber['name'])
```

### Update Subscriber

```python
result = client.update_subscriber(
    email="john@example.com",
    name="John Updated",
    fields={"plan": "premium"}
)
```

### Delete Subscriber

```python
result = client.delete_subscriber("john@example.com")
```

### Add Subscribers to Group

```python
result = client.add_subscribers_to_group(
    group_id="group123",
    emails=["john@example.com", "jane@example.com"]
)
```

### Remove Subscribers from Group

```python
result = client.remove_subscribers_from_group(
    group_id="group123",
    emails=["john@example.com"]
)
```

## Webhook Handling

```python
signature = request.headers.get('X-Sender-Signature')
event = client.handle_webhook_event(
    payload=request.get_json(),
    signature=signature,
    webhook_secret="your-webhook-secret"
)

if event['event_type'] == 'new_subscriber':
    print(f"New subscriber: {event['subscriber']['email']}")
```

## License

MIT License
