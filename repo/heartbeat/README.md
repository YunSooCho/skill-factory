# Heartbeat

Heartbeat is a community platform for managing users, groups, and communications.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your Heartbeat API key:

1. Sign up at [Heartbeat](https://heartbeat.chat)
2. Go to Settings > API Keys
3. Generate and copy your API key

## Usage

```python
from heartbeat import HeartbeatClient

client = HeartbeatClient(api_key='your-api-key')

# Create a channel
channel = client.create_channel(name='general')

# Create a group
group = client.create_group(name='VIP Customers')

# Create a thread
thread = client.create_thread(
    channel_id='channel-123',
    title='Welcome',
    content='Welcome to the community!'
)

# Send a direct message
message = client.send_direct_message(
    recipient_id='user-123',
    content='Hello! How can we help you?'
)

# Create a comment
comment = client.create_comment(
    thread_id='thread-123',
    content='Great post!'
)

# Add users to group
client.add_to_group(group_id='group-123', user_ids=['user-1', 'user-2'])

# Get channel threads
threads = client.get_channel_threads(channel_id='channel-123')
```

## API Methods

### Users
- `get_user(user_id)` - Get user details
- `delete_user(user_id)` - Delete a user
- `invite_users(user_ids)` - Invite users

### Channels & Threads
- `create_channel(name, **kwargs)` - Create a channel
- `get_channel_threads(channel_id)` - Get channel threads
- `create_thread(channel_id, title, content)` - Create a thread
- `create_comment(thread_id, content)` - Add comment to thread

### Groups
- `create_group(name, **kwargs)` - Create a group
- `add_to_group(group_id, user_ids)` - Add users to group
- `delete_from_group(group_id, user_ids)` - Remove users from group

### Events & Messages
- `create_event(event_data)` - Create an event
- `send_direct_message(recipient_id, content)` - Send direct message