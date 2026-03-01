# JustCall Cloud Phone System Integration

JustCall provides VoIP calling and SMS for business communication.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to JustCall
2. Get API Key and API Secret from settings

## Usage
```python
from justcall import JustcallClient

client = JustcallClient(api_key="your-key", api_secret="your-secret")

# Get call logs
calls = client.get_call_logs()

# Make call
client.make_call({"to": "+1234567890", "agent_number": "+19876543210"})

# Send SMS
client.send_sms({
    "from": "+19876543210",
    "to": "+1234567890",
    "body": "Hello!"
})

# Get SMS logs
sms_logs = client.get_sms_logs()

# Manage contacts
contacts = client.get_contacts()
client.create_contact({
    "first_name": "John",
    "phone": "+1234567890"
})

# Get numbers
numbers = client.get_numbers()
```

## API Methods
- `get_call_logs(limit)` - List call logs
- `get_call(call_id)` - Get call
- `make_call(data)` - Make outbound call
- `send_sms(data)` - Send SMS
- `get_sms_logs(limit)` - List SMS logs
- `get_contacts(limit)` - List contacts
- `create_contact(data)` - Create contact
- `get_numbers()` - List phone numbers