# Wamm App API

Wamm App API integration for WhatsApp messaging.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from wamm_app import WammAppClient

client = WammAppClient(api_token="your_api_token")

# Send text message
result = client.send_text_message(
    phone_number="+1234567890",
    message="Hello from Wamm App!"
)

# Send media message
result = client.send_media_message(
    phone_number="+1234567890",
    media_url="https://example.com/image.jpg",
    media_type="image",
    caption="Check this out!"
)

# Check message status
status = client.get_message_status("msg_123")
```

## Features

- Send text messages via WhatsApp
- Send media messages (image, video, document)
- Check message delivery status
- List sent messages
- Get account information

## API Reference

- `send_text_message(phone_number, message, priority)` - Send text
- `send_media_message(phone_number, media_url, media_type, caption)` - Send media
- `get_message_status(message_id)` - Get status
- `list_messages(phone_number, limit, offset)` - List messages
- `get_account_info()` - Get account info

## Authentication

Requires Wamm App API Token.