# Logiless

Japanese e-commerce and inventory management platform.

## API Key
1. Sign up at [https://logiless.com](https://logiless.com)
2. Go to Settings > API Integration
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from logiless.client import LogilessClient

client = LogilessClient(api_key='your_api_key')

# Get product list
products = client.get_products()

# Update inventory
result = client.update_inventory(item_id='ITEM123', quantity=100)
```