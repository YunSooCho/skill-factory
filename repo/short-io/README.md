# Short.io API Client

Python client for Short.io URL shortener.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from client import ShortIoClient

client = ShortIoClient(api_key="your-api-key")
link = client.get_link_from_path("domain_id", "/path")
```

## License
MIT
