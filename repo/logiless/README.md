# Logiless API Integration

Complete Logiless logistics API client. Supports orders, inventory, and shipping tracking.

## Features
- ✅ Order management
- ✅ Product management
- ✅ Inventory tracking
- ✅ Shipment tracking

## Setup
```bash
export LOGILESS_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from logiless_client import LogilessAPIClient

os.environ['LOGILESS_API_KEY'] = 'your_api_key'

client = LogilessAPIClient()
orders = client.get_orders()
client.close()
```