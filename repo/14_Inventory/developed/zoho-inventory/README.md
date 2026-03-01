# Zoho Inventory

Cloud-based inventory management from Zoho.

## API Key
1. Create account at [https://inventory.zoho.com](https://inventory.zoho.com)
2. Go to Settings > API Keys
3. Generate auth token (authtoken) or use OAuth2

## Installation
```bash
pip install requests
```

## Example
```python
from zoho_inventory.client import ZohoInventoryClient

client = ZohoInventoryClient(authtoken='your_authtoken', organization_id='your_org_id')

# Get items
items = client.get_items()

# Create sales order
result = client.create_sales_order(
    customer_id='CUST001',
    item_id='ITEM123',
    rate=100.00,
    quantity=5
)
```