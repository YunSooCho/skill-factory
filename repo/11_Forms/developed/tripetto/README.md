# Tripetto API

Tripetto API integration for form management.

## Usage

```python
from tripetto import TripettoClient
client = TripettoClient(api_token="your_token")
forms = client.list_forms()
responses = client.get_responses("form_id")
```

## Features
- List forms
- Get responses
- Delete responses

## Authentication
Requires Tripetto API Token.
