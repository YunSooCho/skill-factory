# Next-Engine API Integration

Complete Next-Engine ERP API client. Supports products, orders, customers, and inventory.

## Features
- ✅ Product management
- ✅ Order processing
- ✅ Customer management
- ✅ Inventory tracking

## Setup
```bash
export NEXT_ENGINE_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from next_engine_client import NextEngineAPIClient

os.environ['NEXT_ENGINE_API_KEY'] = 'your_api_key'

client = NextEngineAPIClient()
products = client.get_products()
client.close()
```