# Detrack API Integration

## Overview
Complete Detrack delivery management API client for Yoom automation. Supports order management, delivery tracking, and route optimization.

## Supported Features
- ✅ Create and manage delivery orders
- ✅ Assign orders to drivers
- ✅ Bulk order import
- ✅ Driver management
- ✅ Route optimization
- ✅ Daily reports
- ✅ Webhook notifications
- ✅ Time-based delivery scheduling

## Setup

### 1. Get API Key
Visit https://app.detrack.com/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export DETRACK_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from detrack_client import DetrackAPIClient

os.environ['DETRACK_API_KEY'] = 'your_api_key'

client = DetrackAPIClient()

# Create delivery order
order = client.create_order(
    order_number='ORD-001',
    address='123 Main St, City',
    date='2024-01-20',
    time_from='09:00',
    time_to='12:00',
    assign_to='Driver John',
    remarks='Handle with care'
)

# List orders for date
orders = client.list_orders(date='2024-01-20')

# Optimize route
route = client.optimize_route(
    date='2024-01-20',
    driver='Driver John',
    start_address='Warehouse',
    end_address='Home Base'
)

client.close()
```