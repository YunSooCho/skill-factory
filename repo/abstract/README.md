# Abstract API Integration

## Overview
Implementation of Abstract API services for Yoom automation.

## Supported Features
- ✅ Live Exchange Rates
- ✅ Convert Exchange Rates
- ✅ Phone Number Validation
- ✅ Get Current Time
- ✅ Convert Time
- ✅ IP Geolocation Information
- ✅ Email Validation
- ✅ Country Holidays

## Setup

### 1. Get API Keys
Visit https://app.abstractapi.com/ and create an account. You'll need API keys for:
- Exchange Rates API
- Phone Validation API
- Timezone API
- IP Geolocation API
- Email Validation API
- Holidays API

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_keys = {
    "exchange_rates": "your_exchange_rates_api_key",
    "phone_validation": "your_phone_validation_api_key",
    "timezone": "your_timezone_api_key",
    "ip_geolocation": "your_ip_geolocation_api_key",
    "email_validation": "your_email_validation_api_key",
    "holidays": "your_holidays_api_key"
}
```

## Usage

### Basic Example
```python
import asyncio
from abstract_client import AbstractAPIClient

async def main():
    api_keys = {
        "exchange_rates": "your_key",
        "phone_validation": "your_key",
        # ... other keys
    }

    async with AbstractAPIClient(api_keys=api_keys) as client:
        # Get exchange rates
        rates = await client.live_exchange_rates(base="USD")
        print(f"USD -> EUR: {rates.rates.get('EUR')}")

        # Validate email
        email = await client.email_validation("test@example.com")
        print(f"Valid: {email.is_valid}")

asyncio.run(main())
```

### All Features
See `test_abstract.py` for complete examples.

## Integration Type
- **Type:** API Key
- **Authentication:** Each endpoint requires its own API key
- **Protocol:** HTTPS REST API

## Testability
- ✅ All API actions are testable with valid API keys
- ✅ Free tier available for testing
- ⚠️ Rate limits apply (check Abstract API documentation)

## Notes
- Each Abstract API service requires a separate API key
- Free tier has request limits
- All requests are async for better performance