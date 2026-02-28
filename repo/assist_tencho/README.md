# Assist Tencho Client

A Python client for Assist Tencho POS API - Japanese point-of-sale system for retail and restaurants.

## Features

- **Products**: Manage product catalog
- **Orders**: Complete order management
- **Customers**: Customer database
- **Inventory**: Stock tracking and adjustments
- **Stores**: Multi-store support

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

Set the environment variable:
```bash
export ASSIST_TENCHO_API_KEY="your_api_key"
```

## Usage

```python
from assist_tencho import AssistTenchoClient

client = AssistTenchoClient(api_key="your_key")
products = client.list_products()
orders = client.list_orders()
customers = client.list_customers()
inventory = client.get_inventory()
```

## License

MIT License