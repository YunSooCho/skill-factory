# Chatwork API Client

Python async client for Chatwork team collaboration platform API.

## Features

- Send and receive messages
- Task management
- Room management
- User task tracking
- Webhook event handling
- Rate limiting (5 requests/second)

## Installation

```bash
pip install -r requirements.txt
```

## API Token Setup

1. Visit [Chatwork](https://go.chatwork.com)
2. Sign up or log in to your account
3. Click on your avatar → API Token
4. Click "Generate API Token"
5. Copy your API token and store it securely

## Usage

```python
import asyncio
from chatwork.client import ChatworkClient

async def main():
    api_token = "your_chatwork_api_token"

    async with ChatworkClient(api_token) as client:
        # Send a message
        message_id = await client.send_message(
            room_id=12345678,
            body="[info]Hello from Chatwork API![/info]"
        )
        print(f"Sent message: {message_id}")

        # List messages
        messages = await client.list_messages(
            room_id=12345678,
            force=True
        )
        print(f"Retrieved {len(messages)} messages")

        # Create a task
        task_ids = await client.create_task(
            room_id=12345678,
            body="Complete project documentation",
            to_account_ids=[123456789, 987654321]
        )
        print(f"Created tasks: {task_ids}")

        # Get my tasks
        my_tasks = await client.get_my_tasks(status="open")
        print(f"Open tasks: {len(my_tasks)}")

        # List rooms
        rooms = await client.list_rooms()
        print(f"Found {len(rooms)} rooms")

        # Get room info
        room_info = await client.get_room_info(room_id=12345678)
        print(f"Room: {room_info.name}")

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a chat room
2. **List Messages** - Retrieve messages from a room
3. **Create Task** - Create a task in a room
4. **Get My Tasks** - Get tasks assigned to current user
5. **Get Room Info** - Get information about a specific room
6. **List Rooms** - Retrieve all accessible rooms

## Triggers

- **New Message** - Fired when a new message is sent
- **Task Completed** - Fired when a task is completed

## Message Formatting

Chatwork supports message formatting with special tags:

```python
# Add a title
await client.send_message(
    room_id=12345678,
    body="[title]Important Announcement[/title]"
)

# Add information section
await client.send_message(
    room_id=12345678,
    body="[info]This is an information message[/info]"
)

# Add code block
await client.send_message(
    room_id=12345678,
    body="[code]print('Hello, World!')[/code]"
)

# Mention a user
await client.send_message(
    room_id=12345678,
    body="[To:123456789]John, please check this![/to]"
)
```

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message_created":
        message = result["message"]
        print(f"New message: {message.body}")
    elif result["event_type"] == "task_created":
        task = result["task"]
        print(f"New task: {task.body}")
```

## Documentation

- [Chatwork API Documentation](https://developer.chatwork.com/)
- Chatwork Platform: https://go.chatwork.com
- API Base URL: `https://api.chatwork.com/v2`
- Rate Limit: 5 requests per second

## Error Handling

The client will raise exceptions on failed requests. Always wrap API calls in try-except blocks:

```python
try:
    message_id = await client.send_message(room_id=123, body="Hello")
except Exception as e:
    print(f"Error sending message: {e}")
```