# Weclapp

Cloud ERP software for small and medium businesses.

## API Key
1. Sign up at [https://weclapp.com](https://weclapp.com)
2. Go to Administration > API Keys
3. Generate API key

## Installation
```bash
pip install requests
```

## Example
```python
from weclapp.client import WeclappClient

client = WeclappClient(api_key='your_api_key')

# Get articles
articles = client.get_articles()

# Create order
result = client.create_order(
    order_items=[{'articleId': 'ART123', 'quantity': 5}]
)
```