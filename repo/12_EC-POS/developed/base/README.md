# base

Base CRM and business management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from base import BaseClient

client = BaseClient(
    api_key="your-api-key"
)

result = client.list_products()
```

## Features

- Complete API coverage
- Authentication handling
- Request/response validation
- Error handling
- Python 3.8+ support

## Configuration

```bash
export BASE_API_KEY="your-api-key"
```

## License

MIT
