# Sendle API Integration

Complete Sendle shipping API client. Supports quotes, orders, labels, and tracking.

## Features
- ✅ Get shipping quotes
- ✅ Create shipping orders
- ✅ Print shipping labels
- ✅ Track shipments
- ✅ Cancel orders

## Setup
```bash
export SENDLE_API_KEY="your_api_key"
pip install -r requirements.txt
```

## Usage
```python
import os
from sendle_client import SendleAPIClient

os.environ['SENDLE_API_KEY'] = 'your_api_key'

client = SendleAPIClient()

# Get quote
quote = client.get_quotes(
    pickup={'suburb': 'Sydney', 'postcode': '2000'},
    delivery={'suburb': 'Melbourne', 'postcode': '3000'},
    weight=1.5
)

# Create order
order = client.create_order({
    'pickup': quote['pickup'],
    'delivery': quote['delivery'],
    'weight': 1.5
})

client.close()
```