# Asana API Client

Python async client for Asana project management API.

## Features

- Task management (52 actions)
- Project management
- Section management
- User & workspace operations
- Attachments
- Custom fields
- Status updates
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from asana_client import AsanaClient

async def main():
    access_token = "your_token"

    async with AsanaClient(access_token) as client:
        # List workspaces
        workspaces = await client.list_workspaces()

        # Create task
        task = await client.create_task(
            workspace_id=workspaces[0].gid,
            name="Complete project"
        )

asyncio.run(main())
```

## API Actions (52)

Major actions include:
- Task CRUD and management (29 actions)
- Project management (7 actions)
- Section management (6 actions)
- User & workspace operations (5 actions)
- Attachments (4 actions)
- Custom fields (3 actions)

## Triggers

- New Task Added to Project
- Task Completed in Project
- Task Created/Updated in Section
- Project Created (Webhook)
- Section Task Completed
- New Task Added to Section
- Task Created/Updated in Project

## Documentation

- [Asana API Documentation](https://developers.asana.com/reference/)