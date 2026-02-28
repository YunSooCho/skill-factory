# Sendcloud API Integration

Complete Sendcloud shipping API client. Supports shipments, labels, and carrier integration.

## Features
- ✅ Create shipping parcels
- ✅ Print shipping labels
- ✅ Carrier management
- ✅ Parcel tracking
- ✅ Return portals

## Setup
```bash
export SENDCLOUD_API_KEY="your_api_key"
export SENDCLOUD_API_SECRET="your_api_secret"
pip install -r requirements.txt
```

## Usage
```python
import os
from sendcloud_client import SendcloudAPIClient

os.environ['SENDCLOUD_API_KEY'] = 'your_api_key'
os.environ['SENDCLOUD_API_SECRET'] = 'your_api_secret'

client = SendcloudAPIClient()

parcel = client.create_parcel({
    'address': {'name': 'John Doe', 'postal_code': '12345', 'country': 'US'},
    'shipment': {'weight': 1000}
})

client.print_label(parcel['id'])
client.close()
```