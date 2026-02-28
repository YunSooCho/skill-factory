# Appcues API Client

Python async client for Appcues user onboarding API.

## Features

- Flow management
- User profile management
- Event tracking
- Checklist management
- Experience launching
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from appcues_client import AppcuesClient

async def main():
    account_id = "your_account_id"
    api_key = "your_api_key"

    async with AppcuesClient(account_id, api_key) as client:
        # List flows
        flows = await client.list_flows(state="published")

        # Create user event
        await client.create_user_event(
            user_id="user_123",
            event_name="signed_up"
        )

asyncio.run(main())
```

## API Actions

- Flow Management (create, get, update, list)
- User Profile Management
- Event Creation
- Checklist Management
- Experience Launch

## Triggers

- User Completes Flow
- User Starts Flow
- User Dismisses Flow
- Checklist Item Completed

## Documentation

- [Appcues Documentation](https://docs.appcues.com/)