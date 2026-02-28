# adobe-sign

Adobe Sign electronic signature

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from adobe_sign import AdobeSignClient

client = AdobeSignClient(
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
export ADOBE_SIGN_API_KEY="your-api-key"
```

## License

MIT
