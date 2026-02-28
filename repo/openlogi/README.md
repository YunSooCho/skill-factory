# Openlogi API Integration

Complete Openlogi shipping API client. Supports orders, inventory, and delivery tracking.

## Features
- ✅ Order management
- ✅ Product management
- ✅ Inventory tracking
- ✅ Delivery status tracking

## Setup
```bash
export OPENLOGI_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from openlogi_client import OpenlogiAPIClient

os.environ['OPENLOGI_API_KEY'] = 'your_api_key'

client = OpenlogiAPIClient()
orders = client.get_orders()
client.close()
```