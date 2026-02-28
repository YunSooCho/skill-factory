# Digistore Client

A Python client for Digistore24 API - European digital goods platform.

## Features

- **Products**: Digital product management
- **Orders**: Order processing
- **Customers**: Customer management
- **Affiliates**: Affiliate program management
- **Sales**: Sales tracking
- **Payouts**: Commission management

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export DIGISTORE_API_KEY="your_api_key"
```

## Usage

```python
from digistore import DigistoreClient

client = DigistoreClient(api_key="your_key")
products = client.list_products(product_type="download")
sales = client.list_sales(por product_id="prod123")
```

## License

MIT License
