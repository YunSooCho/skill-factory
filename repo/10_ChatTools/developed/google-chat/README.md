# Google Chat API Client

Python async client for Google Chat messaging platform API.

## Features

- Send and update messages
- Space (room) management
- Card-based rich messages
- Thread support
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## Service Account Setup

1. Visit [Google Cloud Console](https://console.cloud.google.com)
2. Create or select a project
3. Go to APIs & Services → Credentials
4. Create a Service Account
5. Download the JSON key file
6. Enable Google Chat API in your project
7. Add the service account as a member to your Google Workspace spaces

## Usage

```python
import asyncio
from google_chat.client import GoogleChatClient

async def main():
    service_account_email = "your-service-account@project.iam.gserviceaccount.com"
    private_key = "-----BEGIN PRIVATE KEY-----\n...your private key...\n-----END PRIVATE KEY-----"

    async with GoogleChatClient(service_account_email, private_key) as client:
        # List spaces
        spaces = await client.list_spaces(page_size=20)
        print(f"Found {len(spaces)} spaces")

        if spaces:
            space_name = spaces[0].name

            # Send a message
            message = await client.send_message(
                space_name=space_name,
                text="Hello from Google Chat API!"
            )
            print(f"Sent message: {message.name}")

            # Send a message with cards
            message_with_card = await client.send_message(
                space_name=space_name,
                cards=[{
                    "header": {"title": "Card Title", "subtitle": "Subtitle"},
                    "sections": [{
                        "widgets": [{
                            "textParagraph": {"text": "Card content here"}
                        }]
                    }]
                }]
            )

            # Get space info
            space = await client.get_space(space_name=space_name)
            print(f"Space: {space.display_name}")

            # Update a message
            updated_message = await client.update_message(
                message_name=message.name,
                text="Updated message content"
            )

            # Delete a message
            await client.delete_message(message_name=message.name)

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a space
2. **List Spaces** - List accessible spaces
3. **Get Space** - Get space details
4. **Create Message** - Create a message in a space
5. **Update Message** - Update an existing message
6. **Delete Message** - Delete a message

## Space Types

- `SPACE` - Chat rooms
- `DM` - Direct messages
- `GROUP_DM` - Group direct messages

## Card Messages

Create rich interactive cards:

```python
cards = [{
    "header": {
        "title": "Deployment Status",
        "subtitle": "Production",
        "imageUrl": "https://example.com/icon.png"
    },
    "sections": [{
        "widgets": [{
            "textParagraph": {"text": "Deployment completed successfully!"}
        }, {
            "buttonList": {
                "buttons": [{
                    "text": "View Logs",
                    "onClick": {"openLink": {"url": "https://example.com/logs"}}
                }]
            }
        }]
    }]
}]
```

## Triggers

- **Message Added** - Fired when a new message is added
- **Space Updated** - Fired when a space is updated

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "MESSAGE":
        message = result["message"]
        print(f"New message: {message.text}")
```

## Documentation

- Google Chat API: https://developers.google.com/chat
- API Base URL: `https://chat.googleapis.com/v1`

## Error Handling

```python
try:
    message = await client.send_message(
        space_name="spaces/AAAAbbbbb",
        text="Hello"
    )
except Exception as e:
    print(f"Error: {e}")
```