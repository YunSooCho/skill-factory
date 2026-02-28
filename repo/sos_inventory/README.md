# SOS Inventory

Manufacturing and inventory management platform.

## API Key
1. Sign up at [https://sosinventory.com](https://sosinventory.com)
2. Navigate to Settings > API Access
3. Generate API credentials

## Installation
```bash
pip install requests
```

## Example
```python
from sos_inventory.client import SOSInventoryClient

client = SOSInventoryClient(api_key='your_api_key')

# Get inventory
inventory = client.get_inventory()

# Create sales order
result = client.create_sales_order(
    customer_id='CUST001',
    items=[{'product_id': 'PROD1', 'quantity': 5}]
)
```