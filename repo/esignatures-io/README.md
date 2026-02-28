# esignatures-io

eSignatures.io service

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from esignatures_io import EsignaturesIoClient

client = EsignaturesIoClient(
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
export ESIGNATURES_IO_API_KEY="your-api-key"
```

## License

MIT
