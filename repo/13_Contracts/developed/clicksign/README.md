# clicksign

ClickSign electronic signature

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from clicksign import ClicksignClient

client = ClicksignClient(
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
export CLICKSIGN_API_KEY="your-api-key"
```

## License

MIT
