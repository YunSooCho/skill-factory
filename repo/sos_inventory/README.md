# SOS Inventory API Integration

## Overview
Complete SOS Inventory management API client for Yoom automation. Supports items, sales orders, purchase orders, warehouses, and inventory management.

## Supported Features
- ✅ Create and manage items
- ✅ Sales order management
- ✅ Purchase order management
- ✅ Customer and vendor management
- ✅ Multi-warehouse inventory
- ✅ Inventory level tracking
- ✅ Inventory adjustments
- ✅ Inventory reports

## Setup

### 1. Get API Key
Visit https://www.sosinventory.com/settings/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export SOS_INVENTORY_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from sos_inventory_client import SosInventoryAPIClient

os.environ['SOS_INVENTORY_API_KEY'] = 'your_api_key'

client = SosInventoryAPIClient()

# Create item
item = client.create_item(
    name='Product A',
    sku='PROD-001',
    description='Sample product',
    cost_price=10.00,
    selling_price=15.00
)

# Create sales order
order = client.create_sales_order(
    customer_id='cust_123',
    items=[
        {'item_id': item['id'], 'quantity': 10, 'price': 15.00}
    ],
    order_date='2024-01-15'
)

# Check inventory levels
levels = client.get_inventory_levels(warehouse_id='wh_456')

# Adjust inventory
client.adjust_inventory(
    item_id=item['id'],
    warehouse_id='wh_456',
    quantity=-5,
    reason='Sale'
)

client.close()
```