# Next-Engine

Japanese integrated ERP and inventory management system.

## API Key
1. Sign up at [https://next-engine.com](https://next-engine.com)
2. Go to Settings > API Configuration
3. Generate API key and sign key

## Installation
```bash
pip install requests
```

## Example
```python
from next_engine.client import NextEngineClient

client = NextEngineClient(api_key='your_api_key', sign_key='your_sign_key')

# Get product list
products = client.get_products()

# Register order
result = client.register_order(order_data={'customer_id': 'CUST001', 'items': [...]})
```