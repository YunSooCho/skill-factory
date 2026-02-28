# Help Scout

Help Scout is a customer support platform for managing customer emails and conversations.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Help Scout API key:

1. Sign up at [Help Scout](https://www.helpscout.com)
2. Go to Your Account > API Key
3. Generate and copy your API key

## Usage

```python
from help_scout import HelpScoutClient

client = HelpScoutClient(api_key='your-api-key')

# Search conversations
conversations = client.search_conversations(query='support')

# Create a customer
customer = client.create_customer({
    'firstName': 'John',
    'lastName': 'Doe',
    'emails': [{'value': 'john@example.com'}]
})

# Create a conversation
conversation = client.create_conversation({
    'subject': 'Support Request',
    'customer': {'id': customer['id']},
    'mailbox': {'id': 123}
})

# Send a reply
reply = client.create_reply(
    conversation_id='conv-123',
    text='Thank you for contacting us!'
)

# Add a note
note = client.add_conversation_note(
    conversation_id='conv-123',
    text='Internal note: Customer is waiting'
)

# Search customers
customers = client.search_customer(query='john')

# Update customer properties
client.update_customer_properties(
    customer_id='customer-123',
    properties={'vip': True}
)

# Get mailboxes
mailboxes = client.get_mailbox_list()

# Get tags
tags = client.get_tag_list()
```

## API Methods

### Conversations
- `create_conversation(conversation_data)` - Create a conversation
- `update_conversation(conversation_id, data)` - Update a conversation
- `search_conversations(query, **kwargs)` - Search conversations
- `create_reply(conversation_id, text)` - Create a reply
- `add_conversation_note(conversation_id, text)` - Add a note
- `update_tags(conversation_id, tags)` - Update conversation tags

### Customers
- `create_customer(customer_data)` - Create a customer
- `get_customer(customer_id)` - Get customer details
- `search_customer(query)` - Search customers
- `update_customer_properties(customer_id, properties)` - Update properties
- `get_customer_properties(customer_id)` - Get customer properties

### Other
- `get_user(user_id)` - Get user details
- `get_mailbox_list()` - List mailboxes
- `get_tag_list()` - List tags
- `get_company_report()` - Get company report