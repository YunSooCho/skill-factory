# Capsule CRM API Client

Python client for Capsule CRM API.

## Features

- Parties: Manage people and organizations
- Opportunities: Sales opportunities with milestones
- Projects: Project management
- Tasks: Task tracking

## Installation

```bash
pip install aiohttp
```

## API Actions (21)

Full CRUD for parties, opportunities, projects, tasks

## Triggers (10)

- Completed Task
- Updated/New/Deleted/Closed Opportunity, Party, Project, Task
- Updated to Specified Opportunity Milestone

## Usage

```python
import asyncio
from capsule_crm import CapsuleCRMClient

async def main():
    client = CapsuleCRMClient(api_token="your_token")

    # Create person
    person = await client.create_party({
        "type": "person",
        "firstName": "John",
        "lastName": "Doe",
        "emailAddresses": [{"address": "john@example.com"}]
    })
    print(f"Person: {person.id}")

    # Create opportunity
    opp = await client.create_opportunity({
        "name": "Big Deal",
        "partyId": person.id,
        "value": 10000,
        "currency": "USD"
    })
    print(f"Opportunity: {opp.id}")

    # Create task
    task = await client.create_task({
        "description": "Follow up",
        "partyId": person.id
    })
    print(f"Task: {task.id}")

    # Search parties
    parties = await client.search_party(firstName="John")
    print(f"Found {len(parties)} parties")

asyncio.run(main())
```

## Authentication

Get API token from Capsule CRM account settings.

## License

MIT