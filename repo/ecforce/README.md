# ECForce Client

A Python client for ECForce API - Japanese e-commerce platform.

## Features

- **Products**: Full product management
- **Orders**: Order processing
- **Customers**: CRM
- **Inventory**: Stock control
- **Categories**: Product categories
- **Webhooks**: Event notifications

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export ECFORCE_API_KEY="your_key"
export ECFORCE_API_SECRET="your_secret"
```

## Usage

```python
from ecforce import EcforceClient

client = EcforceClient(api_key="your_key", api_secret="your_secret")
products = client.list_products()
order = client.create_order({...})
```

## License

MIT License
