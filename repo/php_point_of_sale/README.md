# PHP Point of Sale Client

A Python client for PHP Point of Sale API - Open source POS system.

## Features

- **Items**: Product/item management
- **Sales**: Sales transactions
- **Customers**: Customer management
- **Suppliers**: Supplier management
- **Inventory**: Stock tracking
- **Employees**: Staff management
- **Reports**: Sales reports

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export PHPPOS_API_KEY="your_api_key"
# OR
export PHPPOS_USERNAME="username"
export PHPPOS_PASSWORD="password"
export PHPPOS_BASE_URL="https://your-store.com"
```

## Usage

```python
from php_point_of_sale import PhppointofsaleClient

client = PhppointofsaleClient(api_key="your_key")
items = client.list_items()
sale = client.create_sale({...})
report = client.get_daily_report("2024-01-15")
```

## License

MIT License
