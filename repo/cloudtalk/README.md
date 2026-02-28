# Cloudtalk

Cloudtalk is a cloud-based phone system for customer support.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Cloudtalk API key:

1. Sign up at [Cloudtalk](https://www.cloudtalk.io)
2. Go to Settings > Integrations > API
3. Generate and copy your API key

## Usage

```python
from cloudtalk import CloudtalkClient

# Initialize the client
client = CloudtalkClient(api_key='your-api-key')

# Create a contact
contact = client.create_contact({
    'firstName': 'John',
    'lastName': 'Doe',
    'phone': '+1234567890',
    'email': 'john@example.com'
})
print(f"Created contact: {contact}")

# Search contacts
contacts = client.search_contact(query='John')
print(f"Found {len(contacts)} contacts")

# Get a specific contact
contact = client.get_contact(contact_id='contact-123')
print(f"Contact: {contact}")

# Update a contact
updated = client.update_contact(contact_id='contact-123', data={'phone': '+0987654321'})
print(f"Updated contact: {updated}")

# Send an SMS
sms = client.send_sms(
    phone_number='+1234567890',
    message='Your booking is confirmed!'
)
print(f"Sent SMS: {sms}")

# Delete a contact
result = client.delete_contact(contact_id='contact-123')
print(f"Deleted contact: {result}")
```

## API Methods

- `create_contact(contact_data)` - Create a new contact
- `get_contact(contact_id)` - Get a specific contact
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `search_contact(query)` - Search contacts
- `send_sms(phone_number, message, **kwargs)` - Send an SMS message