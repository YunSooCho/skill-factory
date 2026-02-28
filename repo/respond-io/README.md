# Respond.io

Respond.io is a customer messaging platform for managing conversations across channels.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Respond.io API key:

1. Sign up at [Respond.io](https://www.respond.io)
2. Go to Settings > Developer > API Keys
3. Generate and copy your API key

## Usage

```python
from respond_io import RespondIoClient

client = RespondIoClient(api_key='your-api-key')

# Create or update a contact
contact = client.create_update_contact({
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Create a contact
contact = client.create_contact({
    'name': 'Jane Doe',
    'phone': '+1234567890'
})

# Get contact details
contact = client.get_contact(contact_id='contact-123')

# Update a contact
client.update_contact(contact_id='contact-123', data={'name': 'Jane Smith'})

# Search contacts
contacts = client.search_contacts(query='john')

# Add tag to contact
client.add_tag_to_contact(contact_id='contact-123', tag='VIP')

# Remove tag from contact
client.delete_tag_from_contact(contact_id='contact-123', tag='VIP')

# Delete contact
client.delete_contact(contact_id='contact-123')

# Send a message
message = client.send_message({
    'contact_id': 'contact-123',
    'text': 'Hello! How can we help you?'
})

# Create a comment on conversation
comment = client.create_comment(
    conversation_id='conv-123',
    message='Internal note about the conversation'
)

# Assign conversation
client.assign_conversation(conversation_id='conv-123', user_id='user-456')

# Open or close conversation
client.open_close_conversation(conversation_id='conv-123', closed=True)
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `create_update_contact(contact_data)` - Create or update a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `search_contacts(query)` - Search contacts
- `add_tag_to_contact(contact_id, tag)` - Add a tag
- `delete_tag_from_contact(contact_id, tag)` - Remove a tag

### Conversations
- `send_message(message_data)` - Send a message
- `create_comment(conversation_id, message)` - Add a comment
- `assign_conversation(conversation_id, user_id)` - Assign conversation
- `open_close_conversation(conversation_id, closed)` - Open or close conversation