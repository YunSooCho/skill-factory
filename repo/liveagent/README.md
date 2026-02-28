# LiveAgent

LiveAgent is a help desk and live chat platform for managing customer support.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your LiveAgent API key:

1. Sign up at [LiveAgent](https://www.ladesk.com)
2. Go to Configuration > API
3. Generate and copy your API key

## Usage

```python
from liveagent import LiveagentClient

client = LiveagentClient(api_key='your-api-key', base_url='https://yourcompany.ladesk.com')

# Create a contact
contact = client.create_contact({
    'firstname': 'John',
    'lastname': 'Doe',
    'email': 'john@example.com',
    'phone': '+1234567890'
})

# Get contact details
contact = client.get_contact(contact_id='123')

# Update a contact
client.update_contact(contact_id='123', data={'firstname': 'Jane'})

# List contacts
contacts = client.list_contacts()

# Delete a contact
client.delete_contact(contact_id='123')

# Create a contact group
group = client.create_contact_group(name='VIP Customers')

# List contact groups
groups = client.list_contact_groups()

# List tickets
tickets = client.list_tickets()

# Get ticket details
ticket = client.get_ticket(ticket_id='456')

# Delete a ticket
client.delete_ticket(ticket_id='456')
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `list_contacts(**params)` - List contacts

### Contact Groups
- `create_contact_group(name, **kwargs)` - Create a contact group
- `get_contact_group(group_id)` - Get contact group details
- `update_contact_group(group_id, data)` - Update a contact group
- `delete_contact_group(group_id)` - Delete a contact group
- `list_contact_groups()` - List contact groups

### Tickets
- `get_ticket(ticket_id)` - Get ticket details
- `list_tickets(**params)` - List tickets
- `delete_ticket(ticket_id)` - Delete a ticket