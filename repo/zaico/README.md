# Zaico API Integration

## Overview
Complete Zaico cloud inventory management API client for Yoom automation. Supports inventory items, stock management, locations, categories, and reporting.

## Supported Features
- ✅ Create and manage inventory items
- ✅ Stock adjustment and history
- ✅ Multi-location inventory
- ✅ Category management
- ✅ Inventory reports
- ✅ Low stock alerts
- ✅ Barcode and QR code generation
- ✅ Webhook notifications
- ✅ User management

## Setup

### 1. Get API Key
Visit https://web.zaico.co.jp/settings/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export ZAICO_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from zaico_client import ZaicoAPIClient

os.environ['ZAICO_API_KEY'] = 'your_api_key'

client = ZaicoAPIClient()

# Create item
item = client.create_item(
    name='Product A',
    sku='PROD-001',
    description='Sample product',
    unit='pieces',
    initial_quantity=100
)

# Adjust stock
client.adjust_stock(
    item_id=item['id'],
    quantity=-10,
    reason='Sale',
    notes='Order #12345'
)

# Get stock history
history = client.get_stock_history(item['id'])

# Get low stock report
low_stock = client.get_low_stock_report()

# Generate QR code
barcode = client.generate_barcode(item['id'], barcode_type='QR')

client.close()
```