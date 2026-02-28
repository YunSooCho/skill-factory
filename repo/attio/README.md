# Attio API Client

Python client for Attio CRM API.

## Features

- Records: Create, read, update, delete records
- Lists: Manage list entries
- Notes & Comments: Add notes and comments
- Tasks: Create and manage tasks
- Error Handling: Comprehensive error handling
- Rate Limiting: Built-in rate limiter

## Installation

```bash
pip install aiohttp
```

## API Actions (13)

1. Create Note
2. Create Comment
3. Search Entry
4. Get List Entry
5. Create Entry
6. Search Record
7. Update Record
8. Get Record
9. Delete Record
10. Delete List Entry
11. Update List Entry
12. Create Record
13. Create Task

## Triggers (13)

- Updated Note
- Deleted Record
- Deleted Entry
- Resolved Comment
- New Record
- New Comment
- Unresolved Comment
- Updated Record
- New Note
- Updated Entry
- New Entry
- New Task
- Updated Task

## Usage

```python
import asyncio
from attio import AttioClient

async def main():
    client = AttioClient(bearer_token="your_token")

    # Create record
    record = await client.create_record("companies", {
        "name": "Acme Corp",
        "website": "https://acme.com"
    })
    print(f"Created record: {record.id}")

    # Search records
    records = await client.search_record("companies", name="Acme")
    print(f"Found {len(records)} records")

asyncio.run(main())
```

## Authentication

Get bearer token from Attio dashboard.

## Error Handling

```python
from attio.attio_client import AttioError

try:
    record = await client.get_record("companies", record_id)
except AttioError as e:
    print(f"Error: {e.message}")
```

## License

MIT