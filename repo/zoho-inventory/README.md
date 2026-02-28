# Zoho Inventory API Integration

Complete Zoho Inventory API client. Supports items, orders, contacts, warehouse, and inventory management.

## Features
- ✅ Item management
- ✅ Sales orders
- ✅ Purchase orders
- ✅ Contact management
- ✅ Warehouse tracking
- ✅ Inventory levels
- ✅ Shipments
- ✅ Invoices

## Setup
```bash
export ZOHO_INVENTORY_API_KEY="your_authtoken"
pip install -r requirements.txt
```

## Usage
```python
import os
from zoho_inventory_client import ZohoInventoryAPIClient

os.environ['ZOHO_INVENTORY_API_KEY'] = 'your_authtoken'

client = ZohoInventoryAPIClient()

# List items
items = client.get_items()

# Create sales order
order = client.create_sales_order({
    'customer_id': 'cust_123',
    'line_items': [
        {'item_id': 'item_456', 'quantity': 10}
    ]
})

# Check inventory
inventory = client.get_inventory(item_id='item_456')

client.close()
```