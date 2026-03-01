# Intercom Customer Messaging Integration

Intercom is a customer messaging platform with chat, bots, and support tools.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to Intercom
2. Go to Developer Hub > Authentication
3. Generate access token

## Usage
```python
from intercom import IntercomClient

client = IntercomClient(access_token="your-token")

# Get conversations
convs = client.get_conversations()

# Send message
client.send_message({
    "message_type": "inapp",
    "from": {"type": "admin", "id": "123"},
    "body": "Hello!"
})

# Manage contacts
contact = client.get_contact("67890")
client.create_contact({
    "role": "user",
    "email": "john@example.com",
    "name": "John Doe"
})

# Get teams
teams = client.get_teams()

# Get admins
admins = client.get_admins()
```

## API Methods
- `send_message(data)` - Send message
- `get_conversations(limit)` - List conversations
- `get_contact(contact_id)` - Get contact
- `create_contact(data)` - Create contact
- `get_leads(limit)` - Get leads
- `get_teams()` - List teams
- `get_admins()` - List admins