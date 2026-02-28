# Lodgify

Lodgify is a vacation rental platform for managing property bookings.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Lodgify API key:

1. Sign up at [Lodgify](https://www.lodgify.com)
2. Go to Settings > Integrations > API
3. Generate and copy your API key

## Usage

```python
from lodgify import LodgifyClient

client = LodgifyClient(api_key='your-api-key')

# Note: Lodgify is primarily a trigger-based integration
# Use webhooks to receive booking updates and status changes
```

## API

Lodgify provides trigger-based webhooks for:
- Received Messages
- Booking Status Changes (Open, Booked, Declined, Tentative)
- Booking Updates
- New Bookings

Contact Lodgify support for webhook configuration.