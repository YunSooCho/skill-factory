# YouSign

Electronic signature and document approval platform.

## API Key
1. Register at [https://yousign.com](https://yousign.com)
2. Go to Settings > API Keys
3. Create production/sandbox API key

## Installation
```bash
pip install requests
```

## Example
```python
from yousign.client import YouSignClient

client = YouSignClient(api_key='your_api_key', mode='prod')

# Create signature procedure
procedure = client.create_procedure(
    name='Contract Signing',
    workflow=[{'email': 'user@example.com'}]
)
```