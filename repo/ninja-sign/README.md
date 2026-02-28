# ninja-sign

NinjaSign cloud signature

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from ninja_sign import NinjaSignClient

client = NinjaSignClient(
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
export NINJA_SIGN_API_KEY="your-api-key"
```

## License

MIT
