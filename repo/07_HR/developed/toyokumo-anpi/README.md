# Toyokumo Anpi Safety Confirmation System Integration

Toyokumo Anpi is a Japanese safety confirmation system used to check employee safety during disasters or emergencies. It enables organizations to quickly confirm the status of all employees and collect emergency contact information.

## Features

- Create and manage safety confirmation requests
- Track employee responses in real-time
- Collect location data during emergencies
- Send reminders to unresponsive employees
- Generate statistics and export reports
- Manage emergency contact information

## Installation

```bash
pip install -e .
```

## API Key Setup

1. Log in to your Toyokumo Anpi account
2. Navigate to Settings > API Keys
3. Generate a new API key
4. Note your organization ID
5. Store them securely

## Usage

```python
from toyokumo_anpi import ToyokumoAnpiClient

# Initialize client
client = ToyokumoAnpiClient(
    api_key="your-api-key",
    organization_id="your-org-id"
)

# Create a safety confirmation request
confirmation = client.create_confirmation(
    title="Earthquake Safety Confirmation",
    message="Please confirm your safety status after the earthquake",
    include_location=True,
    deadline="2024-03-01T18:00:00Z"
)
confirmation_id = confirmation['id']

# Get confirmation details
details = client.get_confirmation(confirmation_id)

# Get all responses
responses = client.get_responses(confirmation_id)
for response in responses:
    print(f"{response['employee_name']}: {response['status']}")
    if 'location' in response:
        print(f"  Location: {response['location']}")

# Get statistics
stats = client.get_statistics(confirmation_id)
print(f"Total: {stats['total']}")
print(f"Safe: {stats['safe_count']}")
print(f"Injured: {stats['injured_count']}")
print(f"Pending: {stats['pending_count']}")

# Send reminder to pending employees
client.send_reminder(confirmation_id)

# Get employee emergency contacts
contacts = client.get_employee_contacts("EMP001")
print(contacts)

# Export responses
export = client.export_responses(confirmation_id, format="csv")
print(f"Download: {export['download_url']}")

# Close confirmation
client.close_confirmation(confirmation_id)

# List all confirmations
confirmations = client.list_confirmations(status="active")
```

## API Methods

### Safety Confirmation
- `create_confirmation(title, message, deadline, include_location)` - Create new confirmation
- `get_confirmation(confirmation_id)` - Get confirmation details
- `list_confirmations(status, limit, offset)` - List confirmations
- `get_statistics(confirmation_id)` - Get confirmation statistics
- `close_confirmation(confirmation_id)` - Close a confirmation

### Response Management
- `get_responses(confirmation_id, status, limit, offset)` - Get employee responses
- `get_employee_status(confirmation_id, employee_id)` - Get individual employee status
- `send_reminder(confirmation_id, employee_ids)` - Send reminders
- `export_responses(confirmation_id, format)` - Export responses

### Employee Management
- `list_employees(department, limit, offset)` - List employees
- `get_employee_contacts(employee_id)` - Get emergency contacts
- `update_employee_contacts(employee_id, contacts)` - Update emergency contacts
- `check_employee_availability(employee_id)` - Check availability
- `get_locations(confirmation_id)` - Get location data

## Response Statuses

- `safe` - Employee is safe
- `injured` - Employee is injured and needs help
- `unknown` - Employee has not responded

## Error Handling

```python
try:
    confirmation = client.create_confirmation(
        title="Emergency",
        message="Confirm your status"
    )
except requests.RequestException as e:
    print(f"Error creating confirmation: {e}")
```

## Use Cases

1. **Natural Disasters**: Quickly confirm employee status during earthquakes, typhoons, or floods
2. **Campus Emergencies**: Check safety during campus lockdowns or incidents
3. **Remote Work**: Ensure remote workers' safety during regional emergencies
4. **Travel Safety**: Confirm status of traveling employees during crises

## Support

For API documentation and support, visit https://www.toyokumo.co.jp/anpi/