# BCart Client

A Python client for BCart EC API - Japanese e-commerce platform for online stores.

## Features

- **Products**: Full product management
- **Orders**: Complete order handling
- **Customers**: CRM functionality
- **Categories**: Product categorization
- **Inventory**: Stock management
- **Webhooks**: Event notifications

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export BCART_API_KEY="your_api_key"
export BCART_BASE_URL="https://api.bcart.jp/v1"
```

## Usage

```python
from bcart import BcartClient

client = BcartClient(api_key="your_key")
products = client.list_products()
order = client.create_order({...})
webhook = client.create_webhook("https://url.com", ["order.created"])
```

## License

MIT License