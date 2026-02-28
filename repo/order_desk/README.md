# Order Desk API Integration

Complete Order Desk order management API client. Supports orders, products, and inventory.

## Features
- ✅ Order management
- ✅ Product management
- ✅ Inventory tracking
- ✅ Order fulfillment

## Setup
```bash
export ORDER_DESK_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from order_desk_client import OrderDeskAPIClient

os.environ['ORDER_DESK_API_KEY'] = 'your_api_key'

client = OrderDeskAPIClient()
orders = client.get_orders()
client.close()
```