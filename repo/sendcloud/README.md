# Sendcloud

Multi-carrier shipping and fulfillment platform.

## API Key
1. Sign up at [https://sendcloud.com](https://sendcloud.com)
2. Go to Settings > API Keys
3. Generate API key and secret

## Installation
```bash
pip install requests
```

## Example
```python
from sendcloud.client import SendcloudClient

client = SendcloudClient(api_key='your_api_key', api_secret='your_api_secret')

# Get carriers
carriers = client.get_carriers()

# Create parcel
parcel = client.create_parcel(
    address={'name': 'John Doe', 'street': 'Main St 123', 'city': 'Amsterdam'},
    parcels=[{'weight': 1000}]
)
```