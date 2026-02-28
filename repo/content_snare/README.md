# Content Snare API

Content Snare API integration for content collection.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from content_snare import ContentSnareClient

client = ContentSnareClient(api_key="your_key")

# List requests
requests = client.list_requests(limit=10)

# Get request details
request = client.get_request("request_id")

# Get request documents
documents = client.get_request_documents("request_id")

# Create request
request = client.create_request(
    client_email="client@example.com",
    request_data={"title": "New Request"}
)
```

## Features

- List content requests
- Get request details
- Get request documents
- Create requests
- Update requests

## API Reference

- `list_requests(status, limit, page)` - List requests
- `get_request(request_id)` - Get request details
- `get_request_documents(request_id)` - Get documents
- `create_request(client_email, request_data)` - Create request
- `update_request(request_id, update_data)` - Update request

## Authentication

Requires Content Snare API Key.