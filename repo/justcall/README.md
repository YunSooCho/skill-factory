# JustCall

JustCall is a cloud-based phone system for business communications.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your JustCall API credentials:

1. Sign up at [JustCall](https://justcall.io)
2. Go to Settings > Integrations > API
3. Copy your API Key and API Secret

## Usage

```python
from justcall import JustcallClient

client = JustcallClient(api_key='your-api-key', api_secret='your-api-secret')

# Create a contact
contact = client.create_contact({
    'first_name': 'John',
    'last_name': 'Doe',
    'phone_numbers': ['+1234567890'],
    'email': 'john@example.com'
})

# Search contacts
contacts = client.search_contact(query='john')

# Get contact details
contact = client.get_contact(contact_id='123')

# Update a contact
client.update_contact(contact_id='123', data={'first_name': 'Jane'})

# Delete a contact
client.delete_contact(contact_id='123')

# Search calls
calls = client.search_call(query='inbound')

# Search SMS messages
sms_list = client.search_sms(query='order')

# Download call recording
download_url = client.download_call_recording(call_id='123')
```

## API Methods

### Contacts
- `create_contact(contact_data)` - Create a contact
- `get_contact(contact_id)` - Get contact details
- `update_contact(contact_id, data)` - Update a contact
- `delete_contact(contact_id)` - Delete a contact
- `search_contact(query)` - Search contacts
- `search_phone_number(query)` - Search by phone number

### Calls
- `search_call(query)` - Search calls
- `search_call_sales_dialer(query)` - Search sales dialer calls
- `get_call_sales_dialer(call_id)` - Get call details
- `download_call_recording(call_id)` - Download call recording

### SMS
- `search_sms(query)` - Search SMS messages