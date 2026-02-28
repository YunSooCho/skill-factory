# Seven_io API Client

Python client for Seven_io SMS service.

## Usage

```python
from client import Seven_ioClient

client = Seven_ioClient(api_key="your-api-key")
client.create_contact(phone="+1234567890", email="john@example.com", name="John Doe")
```

## Actions

- create_contact
- update_contact
- search_contact

## License
MIT
