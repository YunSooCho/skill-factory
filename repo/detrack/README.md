# Detrack

Delivery tracking and vehicle management platform.

## API Key
1. Create account at [https://detrack.com](https://detrack.com)
2. Navigate to Settings > API Keys
3. Generate access token

## Installation
```bash
pip install requests
```

## Example
```python
from detrack.client import DetrackClient

client = DetrackClient(api_key='your_api_key')

# Create delivery
delivery = client.create_delivery(
    order_no='ORD12345',
    address='123 Main St, City',
    deliver_to='John Doe'
)
```