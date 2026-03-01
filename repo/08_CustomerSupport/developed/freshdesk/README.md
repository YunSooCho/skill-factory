# Freshdesk Customer Support Integration

Freshdesk is a cloud-based customer support platform for ticket management.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your Freshdesk account
2. Get API key from profile settings
3. Note your domain (e.g., yourcompany.freshdesk.com)

## Usage
```python
from freshdesk import FreshdeskClient

client = FreshdeskClient(api_key="your-key", domain="yourcompany")

# Get tickets
tickets = client.get_tickets(status="open")

# Get ticket
ticket = client.get_ticket(12345)

# Create ticket
new_ticket = client.create_ticket({
    "subject": "Issue",
    "description": "Problem description",
    "email": "customer@example.com",
    "priority": 2
})

# Update ticket
client.update_ticket(12345, {"status": 2, "priority": 3})

# Manage contacts
contact = client.get_contact(67890)
client.create_contact({"name": "John Doe", "email": "john@example.com"})
```

## API Methods
- `get_tickets(status, page)` - List tickets
- `get_ticket(ticket_id)` - Get ticket
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `delete_ticket(ticket_id)` - Delete ticket
- `get_contacts(page)` - List contacts
- `get_contact(contact_id)` - Get contact
- `create_contact(data)` - Create contact
- `get_companies(page)` - List companies
- `get_agents()` - List agents
- `get_groups()` - List groups

## Status Codes
1 - Open, 2 - Pending, 3 - Resolved, 4 - Closed, 5 - Waiting on Customer