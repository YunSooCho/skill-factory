# Kura-Bugyo

Japanese inventory and warehouse management system (蔵奉行).

## API Key
1. Sign up at [https://kura-bugyo.com](https://kura-bugyo.com)
2. Navigate to Settings > API Access
3. Generate API credentials

## Installation
```bash
pip install requests
```

## Example
```python
from kura_bugyo.client import KuraBugyoClient

client = KuraBugyoClient(api_key='your_api_key')

# List inventory
inventory = client.list_inventory()

# Receive goods
result = client.receive_goods(product_code='P001', quantity=50, location='A-01-01')
```