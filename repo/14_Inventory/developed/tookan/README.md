# Tookan

Field workforce management and task automation platform.

## API Key
1. Sign up at [https://tookan.com](https://tookan.com)
2. Navigate to Settings > API Key
3. Generate API token

## Installation
```bash
pip install requests
```

## Example
```python
from tookan.client import TookanClient

client = TookanClient(api_key='your_api_key')

# Create task
result = client.create_task(
    job_type='pickup',
    job_description='Deliver package',
    customer_email='customer@example.com',
    customer_address='123 Main St, City'
)
```