# certifier

Certifier certificate generation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from certifier import CertifierClient

client = CertifierClient(
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
export CERTIFIER_API_KEY="your-api-key"
```

## License

MIT
