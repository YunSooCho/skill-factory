# MaintainX

Facility maintenance and work order management platform.

## API Key
1. Sign up at [https://maintainx.com](https://maintainx.com)
2. Navigate to Settings > API > Generate Token
3. Create API token

## Installation
```bash
pip install requests
```

## Example
```python
from maintainx.client import MaintainXClient

client = MaintainXClient(api_key='your_api_key')

# List work orders
work_orders = client.list_work_orders()

# Create work order
result = client.create_work_order(
    title='Fix HVAC System',
    priority='high',
    assignee_id='USER123'
)
```