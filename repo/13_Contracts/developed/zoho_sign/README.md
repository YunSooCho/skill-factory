# Zoho Sign

Electronic signature solution from Zoho.

## API Key
1. Create account at [https://zoho.com/sign](https://zoho.com/sign)
2. Go to Settings > API > Authentication
3. Generate authtoken or use OAuth2

## Installation
```bash
pip install requests
```

## Example
```python
from zoho_sign.client import ZohoSignClient

client = ZohoSignClient(authtoken='your_authtoken', email='your@email.com')

# Create document
result = client.create_document(
    file_path='contract.pdf',
    recipient='user@example.com'
)
```