# Monday.com API Client

Python client for Monday.com API with async support.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from monday_client import MondayClient

async def main():
    client = MondayClient(api_token="your_api_token")

    # Create an item
    item = await client.create_item(
        board_id="123",
        group_id="topics",
        item_name="New Project",
        column_values={"status": "Working on it"}
    )
    print(f"Created item: {item.id} - {item.name}")

    # Get items
    items = await client.get_items(board_id="123")
    for item in items:
        print(f"- {item.name}")

    # Add update to item
    update = await client.add_update_to_item(
        item_id="456",
        text="Task completed successfully!"
    )

asyncio.run(main())
```

## Features

- Full CRUD operations for boards, groups, and items
- Column value management
- Updates/comments support
- Tag management
- Webhook handling for triggers
- Rate limiting
- Comprehensive error handling

## Documentation

API documentation: https://developer.monday.com/api-reference

## License

MIT