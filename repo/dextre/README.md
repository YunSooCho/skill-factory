# Dextre API Integration

Complete Dextre warehouse management API client. Supports inventory and order management.

## Features
- ✅ Order management
- ✅ Inventory tracking
- ✅ Fulfillment operations

## Setup
```bash
export DEXTRE_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from dextre_client import DextreAPIClient

os.environ['DEXTRE_API_KEY'] = 'your_api_key'

client = DextreAPIClient()
inventory = client.get_inventory(sku='PROD-001')
client.close()
```