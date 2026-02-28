# SendX API Client

Python client for SendX API - email marketing and contact management.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SendXClient

client = SendXClient(
    api_key="your-api-key",
    webhook_secret="your-webhook-secret"  # Optional
)
```

## API Actions

### Create Contact

```python
result = client.create_contact(
    email="john@example.com",
    first_name="John",
    last_name="Doe",
    attributes={"plan": "pro"}
)
```

### Get Contact

```python
contact = client.get_contact("contact123")
```

### Search Contact

```python
result = client.search_contact("john@example.com")
```

### Update Contact

```python
result = client.update_contact(
    contact_id="contact123",
    first_name="John Updated",
    attributes={"plan": "premium"}
)
```

### Delete Contact

```python
result = client.delete_contact("contact123")
```

### Create List

```python
result = client.create_list("Newsletter")
```

### Get List

```python
result = client.get_list("list123")
```

### Search List

```python
result = client.search_list("Newsletter")
```

### Update List

```python
result = client.update_list("list123", "Newsletter Updated")
```

### Delete List

```python
result = client.delete_list("list123")
```

### Create Tag

```python
result = client.create_tag("VIP")
```

### Get Tag

```python
result = client.get_tag("tag123")
```

### Search Tag

```python
result = client.search_tag("VIP")
```

### Update Tag

```python
result = client.update_tag("tag123", "VIP Customer")
```

### Delete Tag

```python
result = client.delete_tag("tag123")
```

## Webhook Handling

```python
event = client.handle_webhook_event(
    payload=request.get_json(),
    signature=request.headers.get('X-SendX-Signature')
)

if event['event_type'] == 'new_contact':
    print(f"New contact: {event['contact']['email']}")
```

## License

MIT License
