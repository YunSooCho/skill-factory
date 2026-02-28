# gmo-sign

GMO Sign for Japanese market

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from gmo_sign import GmoSignClient

client = GmoSignClient(
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
export GMO_SIGN_API_KEY="your-api-key"
```

## License

MIT
