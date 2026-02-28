# Weclapp API Integration

Complete Weclapp ERP API client. Supports products, orders, customers, and inventory.

## Features
- ✅ Product management
- ✅ Order processing
- ✅ Customer management
- ✅ Inventory tracking
- ✅ Warehouse management

## Setup
```bash
export WECLAPP_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from weclapp_client import WeclappAPIClient

os.environ['WECLAPP_API_KEY'] = 'your_api_key'

client = WeclappAPIClient()
products = client.get_products()
orders = client.get_orders()
client.close()
```