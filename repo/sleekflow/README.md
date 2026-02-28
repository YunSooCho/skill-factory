# Sleekflow

Sleekflow is a messaging platform for business communications across multiple channels.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Sleekflow API key:

1. Sign up at [Sleekflow](https://sleekflow.io)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from sleekflow import SleekflowClient

client = SleekflowClient(api_key='your-api-key')

# Search contacts
contacts = client.search_contacts(query='john@example.com')

# Add or update a contact
contact = client.add_or_update_contact({
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890'
})

# Send message via channel
message = client.send_message_via_channel(
    channel_id='channel-123',
    message_data={
        'text': 'Hello! How can we help you?',
        'recipient_id': 'contact-456'
    }
)

# Create a staff member
staff = client.create_staff({
    'name': 'Jane Smith',
    'email': 'jane@example.com',
    'role': 'agent'
})

# Get conversation analysis data
analytics = client.get_conversation_analysis_data(conversation_id='conv-789')
```

## API Methods

### Contacts
- `search_contacts(query)` - Search contacts
- `add_or_update_contact(contact_data)` - Add or update a contact

### Messages
- `send_message_via_channel(channel_id, message_data)` - Send message via channel

### Staff
- `create_staff(staff_data)` - Create a staff member

### Analytics
- `get_conversation_analysis_data(conversation_id)` - Get conversation analytics