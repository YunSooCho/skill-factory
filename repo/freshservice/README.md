# Freshservice IT Service Desk Integration

Freshservice provides IT service desk and ITSM solutions for internal support.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your Freshservice account
2. Get API key from profile settings
3. Note your domain

## Usage
```python
from freshservice import FreshserviceClient

client = FreshserviceClient(api_key="your-key", domain="yourcompany")

# Get tickets
tickets = client.get_tickets()

# Create IT ticket
ticket = client.create_ticket({
    "subject": "Computer issue",
    "description": "Laptop not starting",
    "requester_id": 123,
    "priority": 1
})

# Manage assets
assets = client.get_assets()
client.create_asset({"name": "MacBook Pro", "asset_type_id": 1})

# Changes
changes = client.get_changes()
client.create_change({"title": "Software upgrade", "description": "Update to OS X"})
```

## API Methods
- `get_tickets(status, page)` - List service requests
- `get_ticket(ticket_id)` - Get ticket
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `get_agents()` - List agents
- `get_requesters(page)` - List users
- `get_assets(page)` - List assets
- `create_asset(data)` - Create asset
- `get_changes(page)` - List changes
- `create_change(data)` - Create change request