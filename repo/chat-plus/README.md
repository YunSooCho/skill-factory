# ChatPlus

ChatPlus is a live chat platform for connecting with website visitors.

## Installation

```bash
pip install -r requirements.txt
```

## API Key

To get your ChatPlus API key:

1. Sign up at [ChatPlus](https://www.chatplus.jp)
2. Go to Settings > API Settings
3. Generate and copy your API key

## Usage

```python
from chat_plus import ChatPlusClient

# Initialize the client
client = ChatPlusClient(api_key='your-api-key')

# Send a message to a chat
message = client.send_message(
    chat_id='chat-123',
    message='Thank you for your message! We will get back to you soon.'
)
print(f"Sent message: {message}")

# Get visitor information
visitor = client.get_visitor_info(visitor_id='visitor-123')
print(f"Visitor info: {visitor}")
```

## API Methods

- `send_message(chat_id, message, **kwargs)` - Send a message to a chat
- `get_visitor_info(visitor_id)` - Get visitor information