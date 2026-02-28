# Jitbit Help Desk Integration

Jitbit provides help desk and ticketing system for customer support.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Jitbit help desk
2. Get API key from settings
3. Note your Helpdesk URL

## Usage
```python
from jitbit import JitbitClient

client = JitbitClient(api_key="your-key", base_url="https://yourcompany.jitbit.com")

# Get ticket
ticket = client.get_ticket(12345)

# Get tickets
tickets = client.get_tickets(start_date="2024-01-01")

# Create ticket
client.create_ticket({
    "Subject": "Support request",
    "Body": "I need help with...",
    "UserEmail": "customer@example.com"
})

# Update ticket
client.update_ticket(12345, {"StatusId": 3})

# Add comment
client.add_comment(12345, "Follow-up scheduled")

# Get categories
categories = client.get_categories()

# Get users
users = client.get_users()
```

## API Methods
- `get_ticket(ticket_id)` - Get ticket
- `get_tickets(start_date, limit)` - List tickets
- `create_ticket(data)` - Create ticket
- `update_ticket(ticket_id, data)` - Update ticket
- `add_comment(ticket_id, comment)` - Add comment
- `get_categories()` - Get categories
- `get_users()` - Get users
- `get_user(user_id)` - Get user