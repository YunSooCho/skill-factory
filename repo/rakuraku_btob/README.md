# Rakuraku BtoB Client

A Python client for Rakuraku BtoB API - Japanese B2B e-commerce platform.

## Features

- **Products**: B2B product catalog
- **Orders**: B2B order management
- **Customers**: Business client management
- **Invoices**: Billing and invoicing
- **Bulk Orders**: Bulk ordering
- **Inventory**: Stock management

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export RAKURAKU_BTOB_API_KEY="your_api_key"
```

## Usage

```python
from rakuraku_btob import RakurakuBtobClient

client = RakurakuBtobClient(api_key="your_key")
products = client.list_products()
order = client.create_bulk_order([...])
invoice = client.create_invoice({...})
```

## License

MIT License
