# Airtable API Client

Python async client for Airtable database API.

## Features

- Record CRUD operations
- File attachments
- Comments
- Search and filtering
- Webhook event handling
- Rate limiting (5 requests/second)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from airtable_client import AirtableClient

async def main():
    access_token = "your_token"
    base_id = "appXXXXXXXXXXXXXX"

    async with AirtableClient(access_token, base_id) as client:
        # Create record
        record = await client.create_record(
            table_name="Contacts",
            fields={"Name": "John", "Email": "john@example.com"}
        )

        # List records
        records = await client.list_records(table_name="Contacts", limit=10)

asyncio.run(main())
```

## API Actions

1. Create Record
2. List Records
3. Create Comment
4. Search Records
5. Delete Record
6. Get Record
7. Attach File to Record
8. Update Record
9. Download Record File

## Triggers

- Record Updated
- Record Created

## Documentation

- [Airtable API Documentation](https://airtable.com/developers/web/api)