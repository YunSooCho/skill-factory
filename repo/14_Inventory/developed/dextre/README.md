# Dextre

Warehouse and inventory management system.

## API Key
1. Sign up at [https://dextre.io](https://dextre.io)
2. Go to Settings > API Access
3. Generate API credentials

## Installation
```bash
pip install requests
```

## Example
```python
from dextre.client import DextreClient

client = DextreClient(api_key='your_api_key')

# Get inventory
inventory = client.get_inventory()

# Adjust stock
result = client.adjust_stock(product_sku='SKU001', quantity=100)
```