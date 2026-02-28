# Groove Help Desk Integration

Groove provides simple, shared inbox customer support for small businesses.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Groove account
2. Get API token from settings

## Usage
```python
from groove import GrooveClient

client = GrooveClient(api_token="your-token")

# Get tickets
tickets = client.get_tickets()

# Get ticket
ticket = client.get_ticket("12345")

# Create ticket
client.create_ticket({
    "subject": "Support request",
    "body": "I need help with...",
    "email": "customer@example.com"
})

# Send message
client.send_message("12345", "Here's the solution")

# Get customers
customers = client.get_customers()
```

## API Methods
- `get_tickets(page)` - List tickets
- `get_ticket(ticket_id)` - Get ticket
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `send_message(ticket_id, message)` - Send message
- `get_customers(page)` - List customers
- `get_customer(customer_id)` - Get customer
- `create_customer(data)` - Create customer
- `get_folders()` - List folders