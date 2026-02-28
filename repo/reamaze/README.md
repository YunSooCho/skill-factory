# Reamaze

Reamaze is a customer support platform for managing conversations and messages.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Reamaze API credentials:

1. Sign up at [Reamaze](https://www.reamaze.com)
2. Go to Settings > API
3. Copy your brand slug, login, and API token

## Usage

```python
from reamaze import ReamazeClient

client = ReamazeClient(
    brand_slug='your-brand',
    login='your-login',
    api_token='your-api-token'
)

# Create a contact
contact = client.create_contact({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Search contacts
contacts = client.search_contacts(query='john')

# Create a conversation
conversation = client.create_conversation({
    'message': {
        'body': 'I need help with my account',
        'recipients': ['john@example.com']
    }
})

# Search conversations
conversations = client.search_conversations(query='account')

# Create a message in a conversation
message = client.create_message(
    conversation_id='conv-123',
    message_data={'body': 'How can we help you?'}
)

# Search messages
messages = client.search_messages(query='help')

# Update a contact
client.update_contact(contact_id='123', data={'name': 'Jane Doe'})
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `update_contact(contact_id, data)` - Update a contact
- `search_contacts(query)` - Search contacts

### Conversations
- `create_conversation(conversation_data)` - Create a conversation
- `search_conversations(query, **params)` - Search conversations

### Messages
- `create_message(conversation_id, message_data)` - Create a message
- `search_messages(query)` - Search messages