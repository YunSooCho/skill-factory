# Rakuraku Repeat Client

A Python client for Rakuraku Repeat API - Japanese recurring billing platform.

## Features

- **Subscriptions**: Complete subscription management
- **Plans**: Billing plan configuration
- **Customers**: Customer management
- **Invoices**: Invoice creation and management
- **Payments**: Payment processing
- **Coupons**: Promo code management
- **Usage**: Metered billing support

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

```bash
export RAKURAKU_REPEAT_API_KEY="your_api_key"
```

## Usage

```python
from rakuraku_repeat import RakurakuRepeatClient

client = RakurakuRepeatClient(api_key="your_key")
sub = client.create_subscription({...})
plans = client.list_plans()
invoice = client.create_invoice({...})
```

## License

MIT License
