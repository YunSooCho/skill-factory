# Cloudgate Uno

Cloudgate Uno is a cloud identity and access management platform that provides user provisioning, group management, and access control for organizations.

## API Documentation

- **Base URL:** `https://api.cloudgateuno.com/v1`
- **Authentication:** Bearer Token
- **Rate Limit:** Varies by plan

## Installation

```bash
pip install -r requirements.txt
```

## Example Usage

```python
from client import CloudgateUnoClient

client = CloudgateUnoClient(api_key="YOUR_API_KEY", tenant_id="YOUR_TENANT_ID")

# Get users
users = client.get_users()
print(f"Users: {users}")

# Get specific user
user = client.get_user("12345")
print(f"User: {user}")

# Create user
user_data = {"name": "John Doe", "email": "john@example.com"}
result = client.create_user(user_data)

# Get groups
groups = client.get_groups()

# Get audit logs
logs = client.get_audit_logs()
```

## error Handling

```python
from client import CloudgateUnoClient, CloudgateUnoError

try:
    client = CloudgateUnoClient(api_key="...", tenant_id="...")
    users = client.get_users()
except CloudgateUnoError as e:
    print(f"Error: {e}")
```

## License

This integration is provided as-is for use with the Yoom platform.