# Dynamic Mockups Client

A Python client for Dynamic Mockups API - Product mockup generation service.

## Features

- **Templates**: Browse mockup templates
- **Generation**: Create custom mockups
- **Batch**: Batch mockup generation
- **Categories**: Template categories
- **Download**: Download generated mockups

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export DYNAMIC_MOCKUPS_API_KEY="your_api_key"
```

## Usage

```python
from dynamic_mockups import DynamicMockupsClient

client = DynamicMockupsClient(api_key="your_key")
templates = client.list_templates(category="tshirt")
mockup = client.generate_mockup("tmpl123", "https://url.com/image.png")
```

## License

MIT License
