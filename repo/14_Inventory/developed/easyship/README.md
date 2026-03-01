# EasyShip

Global shipping and logistics platform.

## API Key
1. Sign up at [https://easyship.com](https://easyship.com)
2. Go to Account > API Keys
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from easyship.client import EasyshipClient

client = EasyshipClient(api_key='your_api_key')

# Get shipping rates
rates = client.get_rates(
    origin_address={'country_code': 'US', 'postal_code': '10001'},
    destination_address={'country_code': 'GB', 'postal_code': 'SW1A1AA'},
    parcels=[{'weight': 1.5, 'length': 30, 'width': 20, 'height': 10}]
)
```