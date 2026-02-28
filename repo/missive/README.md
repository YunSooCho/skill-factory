# Missive

Missive is a team email and chat platform for collaborative communication.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Missive API key:

1. Sign up at [Missive](https://missiveapp.com)
2. Go to Settings > Integrations > API
3. Generate and copy your API key

## Usage

```python
from missive import MissiveClient

client = MissiveClient(api_key='your-api-key')

# Create contacts
contacts = client.create_contacts([
    {'name': 'John Doe', 'email': 'john@example.com'}
])

# Search contacts
contacts = client.search_contacts(query='john')

# Get contact details
contact = client.get_contact_details(contact_id='123')

# Update a contact
client.update_contacts(contact_id='123', data={'name': 'Jane Doe'})

# Get conversation list
conversations = client.get_conversation_list()

# Get conversation details
conversation = client.get_conversation_details(conversation_id='conv-123')

# Get conversation messages
messages = client.get_conversation_messages(conversation_id='conv-123')

# Create a draft message
draft = client.create_draft_message(
    conversation_id='conv-123',
    content='Reply to the message'
)

# Create draft with attachment
draft = client.create_draft_message_with_attachment(
    conversation_id='conv-123',
    content='Here is the file',
    attachment_url='https://example.com/file.pdf'
)

# Send a message
message = client.send_message(
    conversation_id='conv-123',
    content='Hello!'
)
```

## API Methods

### Contacts
- `create_contacts(contacts)` - Create contacts
- `get_contact_details(contact_id)` - Get contact details
- `update_contacts(contact_id, data)` - Update contact
- `search_contacts(query)` - Search contacts

### Conversations
- `get_conversation_list(**params)` - List conversations
- `get_conversation_details(conversation_id)` - Get conversation details
- `get_conversation_messages(conversation_id)` - Get conversation messages

### Messages
- `create_draft_message(**message_data)` - Create a draft
- `create_draft_message_with_attachment(content, attachment_url, **kwargs)` - Create draft with attachment
- `send_message(**message_data)` - Send a message