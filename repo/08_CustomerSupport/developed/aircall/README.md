# Aircall API Client

Python async client for Aircall cloud call center API.

## Features

- Call management (search, retrieve, transcription)
- Contact management (CRUD operations)
- Tag management
- Call sentiment and topic analysis
- Webhook event handling
- Rate limiting (100 requests/minute)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from aircall_client import AircallClient

async def main():
    api_token = "your_token"

    async with AircallClient(api_token) as client:
        # Create contact
        contact = await client.create_contact(
            first_name="John",
            last_name="Doe",
            email="john@example.com"
        )

        # Search calls
        calls = await client.search_calls(limit=10)

asyncio.run(main())
```

## API Actions

1. Delete Tag
2. Search Calls
3. Create Contact
4. Add Tag to Call
5. Create Tag
6. Delete Contact
7. Get Call Summary
8. Get Tags List
9. Search Contacts
10. Update Contact
11. Get Call Transcription
12. Get Contact
13. Get Call
14. Get Call Sentiment
15. Get Topics from a Call

## Triggers

- New Agent Call
- Hungup Call
- Agent Call Declined
- Send Message
- Updated Contact
- New Contact
- Removed Contact
- Ended Call
- New Call

## Documentation

- [Aircall API Documentation](https://developer.aircall.io/)