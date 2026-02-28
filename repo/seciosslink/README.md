# SeciossLink

SeciossLink is a Japanese IAM (Identity and Access Management) and SSO (Single Sign-On) solution for managing users, groups, roles, permissions, and application access.

## API Documentation

- **Base URL:** `https://api.seciossworks.com/v1`
- **Authentication:** Bearer Token + X-Organization-ID header
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import SeciossLinkClient

client = SeciossLinkClient(
    api_key="YOUR_API_KEY",
    organization_id="YOUR_ORGANIZATION_ID"
)

# Get users
users = client.get_users()
print(f"Users: {users}")

# Get user details
user = client.get_user("user_123")

# Create user
user_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "display_name": "John"
}
result = client.create_user(user_data)

# Update user
client.update_user("user_123", {"display_name": "John Updated"})

# Delete user
client.delete_user("user_123")

# Get groups
groups = client.get_groups()

# Create group
group_data = {"name": "Engineering", "description": "Engineering team"}
client.create_group(group_data)

# Add user to group
client.add_user_to_group("group_123", "user_456")

# Remove user from group
client.remove_user_from_group("group_123", "user_456")

# Get roles
roles = client.get_roles()

# Assign role
client.assign_role("user_123", "role_admin")

# Revoke role
client.revoke_role("user_123", "role_admin")

# Get active sessions
sessions = client.get_sessions()

# Revoke session
client.revoke_session("session_123")

# Revoke all user sessions
client.revoke_user_sessions("user_123")

# Get audit logs
logs = client.get_audit_logs()

# Get SSO applications
apps = client.get_applications()

# Grant application access
client.grant_application_access("user_123", "app_slack")

# Revoke application access
client.revoke_application_access("user_123", "app_slack")
```

## Error Handling

```python
from client import SeciossLinkClient, SeciossLinkError

try:
    client = SeciossLinkClient(api_key="...", organization_id="...")
    users = client.get_users()
except SeciossLinkError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.