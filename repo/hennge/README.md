# Hennge

Hennge is a cloud authentication and identity management platform that provides SSO, user management, and access control.

## API Documentation

- **Base URL:** `https://api.hennge.com/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import HenngeClient

client = HenngeClient(
    api_key="YOUR_API_KEY",
    tenant_id="YOUR_TENANT_ID"
)

# Get users
users = client.get_users()
print(f"Users: {users}")

# Get user
user = client.get_user("12345")

# Create user
user_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_user(user_data)

# Update user
client.update_user("12345", {"name": "John Smith"})

# Get groups
groups = client.get_groups()

# Create group
group_data = {"name": "Engineering"}
result = client.create_group(group_data)

# Get user status
status = client.get_user_status("12345")

# Get audit logs
logs = client.get_audit_logs()
```

## Error Handling

```python
from client import HenngeClient, HenngeError

try:
    client = HenngeClient(api_key="...", tenant_id="...")
    users = client.get_users()
except HenngeError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.