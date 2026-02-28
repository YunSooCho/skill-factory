# Assignar API Client

Python async client for Assignar construction management API.

## Features

- Worker management
- Crew management
- Scheduling
- Project management
- Task management
- Timesheets
- Compliance tracking
- OAuth 2.0 authentication

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from assignar_client import AssignarClient

async def main():
    client_id = "your_client_id"
    client_secret = "your_client_secret"

    async with AssignarClient(client_id, client_secret) as client:
        # Create worker
        worker = await client.create_worker(
            first_name="John",
            last_name="Smith",
            email="john.smith@example.com"
        )

        # Schedule worker
        await client.schedule_worker(
            worker_id=worker.worker_id,
            crew_id="crew_123",
            project_id="project_456",
            date="2024-02-28"
        )

asyncio.run(main())
```

## API Actions

- Worker Management (create, get, update)
- Crew Management (create)
- Scheduling (assign to crews/projects)
- Project Management (create, get, update)
- Task Management
- Timesheets (get, submit)
- Compliance Status

## Triggers

- Worker Check-in/Check-out
- Task Completed
- Timesheet Submitted
- Project Status Changed
- Compliance Alert

## Documentation

- [Assignar Developer Portal](https://developer.assignar.com/)