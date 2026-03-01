# CloudTalk Cloud Phone System Integration

CloudTalk provides cloud-based phone system and call center solutions.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to CloudTalk dashboard
2. Get API ID and API Key from settings

## Usage
```python
from cloudtalk import CloudTalkClient

client = CloudTalkClient(api_key="your-key", api_id="your-id")

# Get call logs
calls = client.get_calls()

# Make a call
client.make_call({"to": "+1234567890", "agent_id": "AGENT123"})

# Get contacts
contacts = client.get_contacts()

# Statistics
stats = client.get_statistics("2024-01-01", "2024-01-31")
```

## API Methods
- `get_calls(limit)` - List calls
- `get_call(call_id)` - Get call details
- `make_call(data)` - Make outbound call
- `get_call_recording(call_id)` - Get recording URL
- `get_contacts(limit)` - List contacts
- `create_contact(data)` - Create contact
- `get_agents()` - List agents
- `get_numbers()` - List phone numbers
- `get_statistics(start_date, end_date)` - Get call statistics