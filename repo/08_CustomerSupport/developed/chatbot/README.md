# Chatbot Platform Integration

Chatbot platform enables AI-powered automated conversations with customers.

## Installation
```bash
pip install -e .
```

## API Key Setup
1. Log in to your chatbot account
2. Generate API key in settings

## Usage
```python
from chatbot import ChatbotClient

client = ChatbotClient(api_key="your-api-key")

# Send message to bot
client.send_message(bot_id="BOT123", message="Hello", user_id="USER456")

# Get conversations
conversations = client.get_conversations()

# Manage intents
intents = client.get_intents("BOT123")
client.create_intent("BOT123", {"name": "greeting", "expressions": ["hi", "hello"]})

# Train bot
client.train_bot("BOT123")
```

## API Methods
- `send_message(bot_id, message, user_id)` - Send message to bot
- `get_conversations(limit)` - List conversations
- `get_bots()` - List bots
- `get_intents(bot_id)` - Get bot intents
- `create_intent(bot_id, data)` - Create intent
- `train_bot(bot_id)` - Train bot model