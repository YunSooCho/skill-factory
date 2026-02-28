# Apptivo API Client

Python async client for Apptivo CRM and business automation API.

## Features

- Lead management
- Contact management
- Project management
- Task management
- Invoice operations
- Customer management

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from apptivo_client import ApptivoClient

async def main():
    api_key = "your_key"
    office_key = "your_office_key"

    async with ApptivoClient(api_key, office_key) as client:
        # Create lead
        lead = await client.create_lead(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            company="Example Corp"
        )

        # Convert to customer
        customer = await client.convert_lead_to_customer(
            lead_id=lead.lead_id,
            customer_name="Example Corp"
        )

asyncio.run(main())
```

## API Actions

- Lead Management (create, get, update, search, convert)
- Contact Management (create, get, update)
- Project Management (create, get, update)
- Task Management (create, update)
- Invoice Operations

## Triggers

- New Lead Created
- Lead Converted
- New Contact Added
- Project Status Changed
- Task Completed
- Invoice Paid

## Documentation

- [Apptivo API Documentation](https://www.apptivo.com/public/apidocs.jsp)