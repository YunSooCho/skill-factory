# Tally API

Tally API integration for form management.

## Usage

```python
from tally import TallyClient
client = TallyClient(api_key="your_key")
forms = client.list_forms()
responses = client.get_responses("form_id")
```

## Features
- List forms
- Get responses
- Delete responses

## Authentication
Requires Tally API Key.
