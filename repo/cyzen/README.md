# Cyzen API Client

Complete API client for Cyzen - Japanese sales and field management system.

## Features

- Full API coverage for 17 endpoints
- Appointment/Schedule management
- Report management with sharing
- Spot (location) customer management
- History/route tracking
- Timestamp/location recording
- Complete error handling
- Rate limiting support

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from cyzen_client import CyzenClient

async def main():
    client = CyzenClient(api_key="your_api_key")

    # Create an appointment
    appointment = await client.create_appointment({
        "title": "Client Meeting",
        "start_time": "2024-01-20T10:00:00",
        "customer_id": "123"
    })

    # Get report
    report = await client.get_report("report_id")

    await client.close()

asyncio.run(main())
```

## API Endpoints

### Appointments
- `create_appointment()`, `update_appointment()`, `get_appointment()`, `delete_appointment()`

### Spots (Locations)
- `create_spot()`, `update_spot()`, `get_spot()`, `delete_spot()`
- `create_spot_customer()`, `update_spot_customer()`, `get_spot_customer()`, `delete_spot_customer()`
- `get_spot_share_link()`

### Reports
- `get_report()`, `get_report_share_link()`

### History
- `get_route_history()`, `get_timestamp_history()`

## Error Handling

All methods raise `CyzenAPIError` on API errors.

## Rate Limiting

Automatic rate limiting included.

## Webhooks

Supports 4 webhook triggers for reports, route history, timestamp history, and spot updates.