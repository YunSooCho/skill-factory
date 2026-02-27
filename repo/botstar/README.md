# Botstar API Integration

## Overview
Botstar API for chatbot entity management. Create and manage entities for natural language understanding.

## Supported Features
- ✅ Create Entity Item - Add new entity values
- ✅ Get Entity Item - Retrieve details
- ✅ Update Entity Item - Modify values and synonyms
- ✅ Delete Entity Item - Remove entities
- ✅ Search Entity Items - Find by entity name and query

## Setup

### 1. Get API Key and Bot ID
1. Sign up at [Botstar](https://botstar.com/)
2. Create a bot
3. Go to Settings → API Keys
4. Generate API key and note Bot ID

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure
```python
api_key = "your_api_key"
bot_id = "your_bot_id"
```

## Usage

```python
from botstar_client import BotstarClient

client = BotstarClient(api_key="your_key", bot_id="your_bot_id")

# Create an entity
entity = client.create_entity_item(
    entity_name="city",
    value="Tokyo",
    synonyms=["東京", "Tokyo City"],
    metadata={"country": "Japan"}
)

# Search entities
results = client.search_entity_items(
    entity_name="city",
    query="Tokyo"
)

# Update entity
client.update_entity_item(
    entity.id,
    synonyms=["東京", "Tokyo City", "東京都"]
)

# Delete entity
client.delete_entity_item(entity.id)

client.close()
```

## Integration Type
- **Type:** API Key
- **Authentication:** X-API-Key header
- **Protocol:** HTTPS REST API

## Testability
- ✅ All operations testable with valid API key and bot ID

## Notes
- Entities organize values for intent recognition
- Synonyms improve matching accuracy
- Metadata stores additional information