# Google Workspace Admin SDK Client

A comprehensive Python client for Google Workspace Admin SDK, providing access to 13 API actions for user and group management, plus webhook trigger support.

## Features

- ✅ **13 API Actions**: Complete user and group management
- 🔄 **2 Webhook Triggers**: User created and updated event integration
- 🛡️ **Error Handling**: Comprehensive HTTP error handling
- 🚦 **Rate Limiting**: Built-in rate limiter for API quota management
- 🔐 **OAuth 2.0 Authentication**: Secure credential management
- 📝 **Type Hints**: Complete type annotations

## Installation

```bash
pip install -r requirements.txt
```

## Authentication

Google Workspace Admin SDK requiresOAuth 2.0 authentication with admin scopes.

### Prerequisites

1. Enable the Admin SDK API in your Google Cloud project
2. Create OAuth 2.0 credentials (Desktop app)
3. Ensure your account has Google Workspace super admin privileges

### Method 1: Dictionary Credentials

```python
from google_workspace_client import GoogleWorkspaceClient

client = GoogleWorkspaceClient(
    domain='example.com',
    credentials={
        'access_token': 'ya29.a0Af...',
        'refresh_token': '1//0g...',
        'client_id': 'your-client-id.apps.googleusercontent.com',
        'client_secret': 'your-client-secret'
    }
)
```

### Method 2: Token File

```python
client = GoogleWorkspaceClient(
    domain='example.com',
    token_file='workspace_token.pickle'
)
```

### Method 3: OAuth 2.0 Flow (Interactive)

```python
client = GoogleWorkspaceClient(
    domain='example.com',
    credentials_file='client_secret.json'
)
# This will open a browser for OAuth consent
```

### Setting up Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable **Admin SDK API**
4. Create OAuth 2.0 credentials (Desktop app)
5. Ensure you have admin access to the Google Workspace domain

## API Actions

### User Management

#### 1. Create User
```python
response = client.create_user(
    primary_email='john.doe@example.com',
    given_name='John',
    family_name='Doe',
    password='Initial@Password123',
    suspended=False,
    org_unit_path='/Users'
)
print(response['primaryEmail'])
```

#### 2. Delete User
```python
client.delete_user(user_key='john.doe@example.com')
```

#### 3. Suspend User
```python
client.suspend_user(user_key='john.doe@example.com')
```

#### 4. Require Password Change
```python
client.require_password_change(user_key='john.doe@example.com')
```

#### 5. Search User
```python
users = client.search_user(query='email:*@example.com')
for user in users['users']:
    print(f"{user['name']}: {user['primaryEmail']}")
```

#### 6. List Users
```python
# Get all users
users = client.list_users(max_results=10)

# With filtering
users = client.list_users(
    query='orgUnitPath:/Users',
    max_results=100
)

# With pagination
users = client.list_users(max_results=100)
while users:
    for user in users['users']:
        print(user['primaryEmail'])
    
    if not users.get('nextPageToken'):
        break
    
    users = client.list_users(
        max_results=100,
        page_token=users['nextPageToken']
    )
```

#### 7. Update User
```python
client.update_user(
    user_key='john.doe@example.com',
    givenName='Johnathan',
    suspended=True,
    orgUnitPath='/Managers'
)
```

### Group Management

#### 1. Create Group
```python
group = client.create_group(
    email='sales-team@example.com',
    name='Sales Team',
    description='Sales department group'
)
print(group['email'])
```

#### 2. List Groups
```python
groups = client.list_groups(max_results=10)
for group in groups['groups']:
    print(f"{group['name']}: {group['email']} ({group['directMembersCount']} members)")
```

#### 3. Search Groups
```python
groups = client.search_groups(query='name:*Team*')
for group in groups['groups']:
    print(group['email'])
```

#### 4. Add Member to Group
```python
client.add_member_to_group(
    group_key='sales-team@example.com',
    member_email='john.doe@example.com',
    role='MEMBER'  # or 'MANAGER', 'OWNER'
)
```

#### 5. Remove Member from Group
```python
client.remove_member_from_group(
    group_key='sales-team@example.com',
    member_key='john.doe@example.com'
)
```

#### 6. List Group Members
```python
members = client.list_group_members(
    group_key='sales-team@example.com',
    max_results=100
)

for member in members['members']:
    print(f"{member['email']} ({member['role']})")

# Filter by role
managers = client.list_group_members(
    group_key='sales-team@example.com',
    roles=['MANAGER', 'OWNER']
)
```

## Webhook Triggers

Google Workspace provides event notifications via Google Cloud Pub/Sub.

### Setting Up Pub/Sub Subscriptions

```python
from google_workspace_client import GoogleWorkspaceWebhooks

# Setup user events subscription
user_config = GoogleWorkspaceWebhooks.setup_user_events_subscription(
    project_id='my-gcp-project',
    topic_name='workspace-user-events'
)

# Setup group events subscription
group_config = GoogleWorkspaceWebhooks.setup_group_events_subscription(
    project_id='my-gcp-project',
    topic_name='workspace-group-events'
)

print(user_config['instructions'])
```

### Required Google Cloud Setup

1. **Enable Pub/Sub API** in Google Cloud Console
2. **Create a Pub/Sub topic**:
   ```bash
   gcloud pubsub topics create workspace-user-events
   ```

3. **Create watch using Admin SDK API**:
   ```python
   # This requires additional implementation using the API
   # See: https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/watch
   ```

4. **Subscribe your webhook to the topic**:
   ```bash
   gcloud pubsub subscriptions create user-events-sub \
     --topic workspace-user-events \
     --push-endpoint https://your-server.com/webhook
   ```

### Handling Webhooks

```python
from google_workspace_client import GoogleWorkspaceWebhooks

# In your webhook handler
def handle_incoming_webhook(payload):
    event_type = payload.get('eventType')
    
    if event_type == 'USER_ADD':
        result = GoogleWorkspaceWebhooks.handle_user_created_webhook(payload)
    elif event_type == 'USER_UPDATE':
        result = GoogleWorkspaceWebhooks.handle_user_updated_webhook(payload)
    
    return result
```

## Advanced Usage

### Filtering Users by Organizational Unit

```python
# Get users in specific OU
users = client.list_users(
    query='orgUnitPath:/Sales',
    max_results=50
)
```

### Adding Multiple Users to Group

```python
emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']
for email in emails:
    client.add_member_to_group(
        group_key='sales-team@example.com',
        member_email=email
    )
```

### Managing Admin Users

```python
# List all admins
admins = client.list_users(query='isAdmin=true')

# Promote user to admin
client.update_user(
    user_key='john.doe@example.com',
    isAdmin=True
)
```

### Working with Suspended Users

```python
# List suspended users
suspended = client.list_users(query='suspended=true')

# Unsuspend user
client.update_user(
    user_key='john.doe@example.com',
    suspended=False
)
```

## Rate Limiting

The client includes automatic rate limiting:
- **Default**: 100 calls per 100 seconds
- Adjust via: `client.rate_limiter.max_calls = 200`

## Error Handling

```python
try:
    client.create_user(
        primary_email='john.doe@example.com',
        given_name='John',
        family_name='Doe',
        password='Password123'
    )
except Exception as e:
    # Errors are automatically logged
    print(f"Error: {e}")
```

Common errors:
- `401`: Authentication failed → Refresh credentials
- `403`: Permission denied → Ensure admin account
- `404`: Resource not found → Verify email/ID
- `409`: Resource already exists → Check for duplicates
- `400`: Bad request → Check input validation

## Best Practices

1. **Use service accounts** for automated workflows
2. **Implement retry logic** for transient failures
3. **Cache user/group lists** to reduce API calls
4. **Use pagination** for large directories
5. **Audit trail**: Log all admin operations

## Security Considerations

- Never commit credentials to version control
- Use environment variables for sensitive data
- Implement least-privilege access
- Rotate access tokens regularly
- Enable audit logging in Google Workspace admin console

## Limitations

- **Admin permissions required**: Requires super admin access
- **API rate limits**: Respect quotas and implement rate limiting
- **Webhook complexity**: Requires Google Cloud Pub/Sub setup
- **Domain restrictions**: Cannot manage users outside your domain

## Testing

```python
# Test connection
client = GoogleWorkspaceClient(
    domain='example.com',
    token_file='workspace_token.pickle'
)

# Test list users
users = client.list_users(max_results=1)
if users['users']:
    print(f"Connected! Found users in {client.domain}")
else:
    print("Connected! No users found (or empty domain)")
```

## License

MIT License

## Resources

- [Google Workspace Admin SDK Documentation](https://developers.google.com/admin-sdk/directory)
- [Admin SDK - Users API](https://developers.google.com/admin-sdk/directory/v1/reference/users)
- [Admin SDK - Groups API](https://developers.google.com/admin-sdk/directory/v1/reference/groups)
- [Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)