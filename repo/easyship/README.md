# Easyship API Integration

## Overview
Complete Easyship shipping API client for Yoom automation. Supports shipments, rate calculation, labels, tracking, and courier management.

## Supported Features
- ✅ Create and manage shipments
- ✅ Get shipping rates from multiple couriers
- ✅ Generate shipping labels
- ✅ Shipment tracking
- ✅ Courier account management
- ✅ Address validation
- ✅ Webhook notifications

## Setup

### 1. Get API Key
Visit https://dashboard.easyship.com/account/api to get your API key.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```bash
export EASYSHIP_API_KEY="your_api_key_here"
```

## Usage

```python
import os
from easyship_client import EasyshipAPIClient

os.environ['EASYSHIP_API_KEY'] = 'your_api_key'

client = EasyshipAPIClient()

# Get rates
rates = client.get_rates(
    origin={'city': 'New York', 'country_code': 'US'},
    destination={'city': 'London', 'country_code': 'GB'},
    parcels=[{'length': 10, 'width': 10, 'height': 10, 'weight': 1}]
)

# Create shipment
shipment = client.create_shipment(
    CourierAccountId=rate['courier_account_id'],
    # ... other shipment details
)

# Generate label
label = client.generate_label(shipment['id'])

# Track shipment
tracking = client.track_shipment(shipment['id'])

client.close()
```