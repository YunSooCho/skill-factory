# edusign

EduSign educational signing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from edusign import EdusignClient

client = EdusignClient(
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
export EDUSIGN_API_KEY="your-api-key"
```

## License

MIT
