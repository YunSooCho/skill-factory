# Scribeless API Client

Python client for Scribeless API - handwritten letter service.

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

```python
from client import ScribelessClient

client = ScribelessClient(api_key="your-api-key")
```

## API Actions

### Create Recipient

```python
result = client.create_recipient(
    name="John Doe",
    address_line1="123 Main St",
    city="New York",
    postal_code="10001",
    country_code="US",
    address_line2="Apt 4B",
    email="john@example.com"
)

print(f"Recipient ID: {result['recipient_id']}")
```

## License

MIT License
