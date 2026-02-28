# Zaico

Japanese cloud-based inventory management platform (在庫管理).

## API Key
1. Sign up at [https://zaico.co.jp](https://zaico.co.jp)
2. Go to Settings > API Settings
3. Generate API token

## Installation
```bash
pip install requests
```

## Example
```python
from zaico.client import ZaicoClient

client = ZaicoClient(api_token='your_api_token')

# Get inventory
inventory = client.get_inventory()

# Create item
result = client.create_item(
    title='New Product',
    quantity=100,
    sku='SKU001'
)
```