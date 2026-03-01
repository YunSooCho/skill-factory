# Commerce Robo Client

A Python client for Commerce Robo API - Japanese e-commerce automation platform.

## Features

- **Products**: Product catalog management
- **Orders**: Order synchronization
- **Marketplaces**: Multi-channel integration
- **Automation**: Workflow automation
- **Inventory**: Stock synchronization
- **Reports**: Sales and performance reports

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export COMMERCE_ROBO_API_KEY="your_api_key"
```

## Usage

```python
from commerce_robo import CommerceRoboClient

client = CommerceRoboClient(api_key="your_key")
products = client.list_products(marketplace="rakuten")
client.sync_product("prod123", ["amazon", "rakuten"])
```

## License

MIT License
