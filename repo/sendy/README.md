# Sendy API Client

Python client for Sendy API - self-hosted email newsletter service.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import SendyClient

client = SendyClient(
    api_url="https://sendy.yourdomain.com",
    api_key="your-api-key"
)
```

## API Actions

### Add Subscriber

```python
result = client.add_subscriber(
    email="john@example.com",
    list_id="list123",
    name="John Doe",
    custom_fields={"company": "Acme Corp"}
)
```

### Delete Subscriber

```python
result = client.delete_subscriber(
    email="john@example.com",
    list_id="list123"
)
```

### Unsubscribe User

```python
result = client.unsubscribe_user(
    email="john@example.com",
    list_id="list123"
)
```

### Get Lists

```python
result = client.get_lists()
```

### Get Brands

```python
result = client.get_brands()
```

## License

MIT License
