# Byteplant Phone Validator Integration

## Overview
Implementation of Byteplant Phone Validator API for Yoom automation.

## Supported Features
- ✅ Verify Phone Number (single and bulk validation)

## Setup

### 1. Get API Key
1. Visit [Byteplant Phone Validator](https://www.byteplant.com/phone-number-validation-api)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example
```python
import asyncio
from byteplant_phone_validator_client import ByteplantPhoneValidatorClient

async def main():
    api_key = "your_api_key"

    async with ByteplantPhoneValidatorClient(api_key=api_key) as client:
        # Single number validation
        result = await client.verify_phone_number(
            phone_number="+15551234567",
            country_code="US"
        )

        print(f"Valid: {result.is_valid}")
        print(f"Status: {result.status}")
        print(f"Location: {result.location}")
        print(f"Carrier: {result.carrier}")

asyncio.run(main())
```

### Bulk Validation
```python
async def bulk_example():
    api_key = "your_api_key"

    async with ByteplantPhoneValidatorClient(api_key=api_key) as client:
        phone_numbers = [
            "+15551234567",
            "+442071234567",
            "+81312345678"
        ]

        results = await client.verify_bulk_phone_numbers(phone_numbers)

        for result in results:
            print(f"{result.phone_number}: {'Valid' if result.is_valid else 'Invalid'}")

asyncio.run(bulk_example())
```

### Convenience Function
```python
from byteplant_phone_validator_client import validate_phone

# One-shot validation without context manager
result = asyncio.run(validate_phone(
    api_key="your_api_key",
    phone_number="+15551234567",
    country_code="US"
))

print(result.is_valid)
```

## Integration Type
- **Type:** API Key
- **Authentication:** API key in query parameters
- **Protocol:** HTTPS REST API

## Testability
- ✅ Free trial available (with limited requests)
- ✅ All API actions are testable with valid API key
- ⚠️ Rate limits apply (check API documentation)

## API Response

### PhoneValidationResult
```python
@dataclass
class PhoneValidationResult:
    phone_number: str      # The validated phone number
    is_valid: bool         # Whether the number is valid
    status: str            # Status message (valid, invalid, unknown)
    country_code: Optional[str]  # ISO country code
    location: Optional[str]       # City/region
    carrier: Optional[str]        # Carrier/provider
    line_type: Optional[str]      # Mobile, landline, VOIP, etc.
    error_message: Optional[str]  # Error if validation failed
    raw_response: Dict            # Full API response
```

## Error Handling

The client handles common errors:

- **ValueError**: Invalid parameters or phone number
- **aiohttp.ClientError**: Network errors
- **401 Unauthorized**: Invalid API key
- **429 Rate Limit**: Too many requests

## Notes
- Supports validation of phone numbers from over 230 countries
- Provides detailed information including carrier and line type
- Free trial limited to a certain number of validations
- For bulk validation, contact Byteplant for a commercial plan