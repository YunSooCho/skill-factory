# Superchat

Superchat is a multi-channel messaging platform for managing customer communications.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Superchat API key:

1. Sign up at [Superchat](https://superchat.de)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from superchat import SuperchatClient

client = SuperchatClient(api_key='your-api-key')

# Create a contact
contact = client.create_contact({
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890'
})

# Get contact details
contact = client.get_contact(contact_id='contact-123')

# Update a contact
client.update_contact(contact_id='contact-123', data={'name': 'Jane Doe'})

# Search contacts
contacts = client.search_contact(query='john@example.com')

# Send a message
message = client.send_message({
    'channel_id': 'channel-456',
    'recipient_id': 'contact-123',
    'text': 'Hello! How can we help you?'
})

# Send an email
email = client.send_email({
    'to': 'customer@example.com',
    'subject': 'Support Request',
    'body': 'Thank you for contacting us!'
})

# Create a note
note = client.create_note({
    'contact_id': 'contact-123',
    'content': 'Internal note about the customer'
})

# Get note details
note = client.get_note(note_id='note-789')

# Update a note
client.update_note(note_id='note-789', content='Updated note content')

# Delete a note
client.delete_note(note_id='note-789')

# Upload a file
file = client.upload_file({
    'name': 'document.pdf',
    'content': 'base64_encoded_content'
})

# Delete a contact
client.delete_contact(contact_id='contact-123')
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `search_contact(query)` - Search contacts

### Messages
- `send_message(message_data)` - Send a message
- `send_email(email_data)` - Send an email

### Notes
- `create_note(note_data)` - Create a note
- `get_note(note_id)` - Get note details
- `update_note(note_id, content)` - Update a note
- `delete_note(note_id)` - Delete a note

### Files
- `upload_file(file_data)` - Upload a file