# SignTime

Electronic signature automation and document workflow platform.

## API Key
1. Register at [https://signtime.com](https://signtime.com)
2. Go to API Settings in your dashboard
3. Generate API credentials

## Installation
```bash
pip install requests
```

## Example
```python
from signtime.client import SignTimeClient

client = SignTimeClient(api_key='your_api_key')

# Create signing request
request = client.create_signing_request(
    document_path='/path/to/doc.pdf',
    recipients=['email@example.com']
)

# Check status
status = client.get_status(request['id'])
```