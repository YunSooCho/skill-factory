# Openlogi

Japanese cloud-based fulfillment and warehouse service.

## API Key
1. Sign up at [https://openlogi.com](https://openlogi.com)
2. Navigate to Settings > API Integration
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from openlogi.client import OpenlogiClient

client = OpenlogiClient(api_key='your_api_key')

# Get warehouse inventory
inventory = client.get_inventory()

# Create shipment order
result = client.create_shipment(
    order_code='ORD001',
    items=[{'sku': 'SKU001', 'quantity': 2}]
)
```