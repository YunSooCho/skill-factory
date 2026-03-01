# docusign

DocuSign signature management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from docusign import DocusignClient

client = DocusignClient(
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
export DOCUSIGN_API_KEY="your-api-key"
```

## License

MIT
