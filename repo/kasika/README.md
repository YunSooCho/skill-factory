# Kasika Customer Support Integration

Kasika provides customer support and help desk solutions.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Kasika account
2. Generate API key from settings

## Usage
```python
from kasika import KasikaClient

client = KasikaClient(api_key="your-key")

# Get tickets
tickets = client.get_tickets(status="open")

# Get ticket
ticket = client.get_ticket("TICKET123")

# Create ticket
client.create_ticket({
    "subject": "Support request",
    "description": "I need help...",
    "customer_email": "customer@example.com"
})

# Update ticket
client.update_ticket("TICKET123", {"status": "in_progress"})

# Add comment
client.add_comment("TICKET123", "Working on this")

# Get customers
customers = client.get_customers()

# Get agents
agents = client.get_agents()
```

## API Methods
- `get_tickets(status, limit)` - List tickets
- `get_ticket(ticket_id)` - Get ticket
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `add_comment(ticket_id, comment)` - Add comment
- `get_customers(limit)` - List customers
- `get_agents()` - List agents