# Wan-Sign

Digital signature solution for business document signing.

## API Key
1. Sign up at [https://wansign.com](https://wansign.com)
2. Navigate to Developer Settings > API Keys
3. Create new API key

## Installation
```bash
pip install requests
```

## Example
```python
from wan_sign.client import WanSignClient

client = WanSignClient(api_key='your_api_key')

# Upload and sign
result = client.upload_and_sign(
    document_path='contract.pdf',
    signers=[{'name': 'John', 'email': 'john@example.com'}]
)
```