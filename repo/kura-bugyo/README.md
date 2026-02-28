# Kura-Bugyo API Integration

Complete Kura-Bugyo warehouse management API client. Japanese warehouse operations support.

## Features
- ✅ Product management
- ✅ Order processing
- ✅ Inventory tracking

## Setup
```bash
export KURA_BUGYO_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from kura_bugyo_client import KuraBugyoAPIClient

os.environ['KURA_BUGYO_API_KEY'] = 'your_api_key'

client = KuraBugyoAPIClient()
products = client.get_products()
client.close()
```