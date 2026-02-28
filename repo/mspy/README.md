# mSpy Monitoring Integration

mSpy provides mobile monitoring and parental control solutions.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to mSpy account
2. Generate API key from developer settings

## Usage
```python
from mspy import MspyClient

client = MspyClient(api_key="your-key")

# Get monitored devices
devices = client.get_devices()

# Get device info
device = client.get_device("DEV123")

# Get activity logs
logs = client.get_activity_logs("DEV123")

# Get location
location = client.get_location("DEV123")

# Get messages
messages = client.get_messages("DEV123")

# Get calls
calls = client.get_calls("DEV123")

# Get app usage
apps = client.get_app_usage("DEV123")

# Set alerts
client.set_alert("DEV123", {
    "type": "location",
    "threshold": "geofence"
})

# Get alerts
alerts = client.get_alerts("DEV123")
```

## API Methods
- `get_devices()` - List monitored devices
- `get_device(device_id)` - Get device info
- `get_activity_logs(device_id, limit)` - Get activity logs
- `get_location(device_id)` - Get current location
- `get_messages(device_id, limit)` - Get messages
- `get_calls(device_id, limit)` - Get call logs
- `get_app_usage(device_id, limit)` - Get app usage
- `set_alert(device_id, data)` - Set monitoring alert
- `get_alerts(device_id)` - Get alerts

## Note
This integration requires proper authorization and consent for monitoring. Ensure compliance with applicable laws and regulations.