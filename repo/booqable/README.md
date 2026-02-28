# Booqable

Rental inventory and equipment management platform.

## API Key
1. Sign up at [https://booqable.com](https://booqable.com)
2. Go to Account > Integrations > API
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from booqable.client import BooqableClient

client = BooqableClient(api_key='your_api_key')

# List available products
products = client.list_products()

# Create order
order = client.create_order(product_id='prod123', quantity=2, customer_id='cust456')
```