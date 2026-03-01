# Xodo Sign

Electronic signature and document management from Xodo.

## API Key
1. Create account at [https://xodo.com](https://xodo.com)
2. Go to Account > API Access
3. Generate API token

## Installation
```bash
pip install requests
```

## Example
```python
from xodo_sign.client import XodoSignClient

client = XodoSignClient(api_key='your_api_key')

# Send for signature
result = client.send_for_signature(
    file_path='document.pdf',
    recipient_email='user@example.com'
)
```