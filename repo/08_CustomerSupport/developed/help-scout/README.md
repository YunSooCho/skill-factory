# Help Scout Customer Support Integration

Help Scout provides email-based customer support with shared inbox features.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Help Scout account
2. Generate API key (app ID and secret) from settings

## Usage
```python
from help_scout import HelpScoutClient

client = HelpScoutClient(api_key="your-key")

# Get conversations
conversations = client.get_conversations(status="active")

# Get conversation
conv = client.get_conversation(12345)

# Create conversation
client.create_conversation({
    "subject": "Help needed",
    "mailboxId": 123,
    "customer": {"email": "customer@example.com"},
    "threads": [{"type": "customer", "body": "I need help"}]
})

# Get mailboxes
mailboxes = client.get_mailboxes()

# Get customers
customers = client.get_customers()
```

## API Methods
- `get_conversations(status, page)` - List conversations
- `get_conversation(conversation_id)` - Get conversation
- `create_conversation(data)` - Create conversation
- `get_mailboxes()` - List mailboxes
- `get_customers(page)` - List customers
- `get_customer(customer_id)` - Get customer
- `create_customer(data)` - Create customer
- `get_threads(conversation_id)` - Get conversation threads

## Status Codes
- active, pending, closed, spam, draft