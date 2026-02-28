# LiveAgent Help Desk Integration

LiveAgent provides comprehensive help desk and live chat customer support.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to LiveAgent
2. Get API key from configuration
3. Note your API URL

## Usage
```python
from liveagent import LiveagentClient

client = LiveagentClient(api_key="your-key", base_url="https://yourcompany.ladesk.com/api")

# Get tickets
tickets = client.get_tickets()

# Get ticket
ticket = client.get_ticket("T12345")

# Create ticket
client.create_ticket({
    "subject": "Support request",
    "message": "I need help...",
    "recipient": "support@company.com"
})

# Update ticket
client.update_ticket("T12345", {"status": "Open"})

# Add message
client.add_message("T12345", "Here's an update")

# Get customers
customers = client.get_customers()

# Get agents
agents = client.get_agents()
```

## API Methods
- `get_tickets(limit)` - List tickets
- `get_ticket(ticket_id)` - Get ticket
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `add_message(ticket_id, message)` - Add message
- `get_customers(limit)` - Get customers
- `get_agents()` - Get agents