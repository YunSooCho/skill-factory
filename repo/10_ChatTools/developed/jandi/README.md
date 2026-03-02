# Jandi API Client

Python async client for Jandi Korean team collaboration platform API.

## Features

- Send messages to topics
- Topic management
- Entity (task/note) management
- Team collaboration
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Jandi](https://lp.yoom.fun/apps/jandi)
2. Sign up or log in to your account (in Korean)
3. Navigate to Settings → API Keys (設定 → API キー)
4. Click "Generate New API Key" (新しい API キーの生成)
5. Copy your API key and store it securely

## Usage

```python
import asyncio
from jandi.client import JandiClient

async def main():
    api_key = "your_jandi_api_key"

    async with JandiClient(api_key) as client:
        # List topics
        topics = await client.list_topics(limit=20)
        print(f"Found {len(topics)} topics")

        if topics:
            topic_id = topics[0].id

            # Send a simple text message
            message_id = await client.send_message(
                topic_id=topic_id,
                body="안녕하세요! Jandi API에서 보낸 메시지입니다."
            )

            # Send a message with connect info (rich format)
            message_id = await client.send_message(
                topic_id=topic_id,
                body="프로젝트 업데이트",
                connect_color="#FAC11B",
                connect_info=[
                    {
                        "title": "완료된 작업",
                        "description": "프론트엔드 개발 완료"
                    },
                    {
                        "title": "다음 단계",
                        "description": "백엔드 API 연동"
                    }
                ]
            )

            # Get topic details
            topic = await client.get_topic(topic_id=topic_id)
            print(f"Topic: {topic.name}")

            # Create an entity
            entity = await client.create_entity(
                topic_id=topic_id,
                title="새로운 작업",
                content="작업 설명을 여기에 입력하세요"
            )

            # List entities
            entities = await client.list_entities(topic_id=topic_id, status="active")
            print(f"Found {len(entities)} entities")

            # Get entity details
            entity_details = await client.get_entity(
                topic_id=topic_id,
                entity_id=entity.id
            )

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a topic
2. **List Topics** - List all topics
3. **Get Topic** - Get topic details
4. **Create Entity** - Create an entity (task/note)
5. **List Entities** - List entities in a topic
6. **Get Entity** - Get entity details

## Message Formatting

Jandi supports rich Connect messages:

```python
connect_info = [
    {
        "title": "제목 1",
        "description": "설명 내용",
        "imageUrl": "https://example.com/image.png"
    },
    {
        "title": "제목 2",
        "description": "다른 설명 내용"
    }
]
```

Available colors:
- `#FAC11B` - Yellow (default)
- `#00A1E9` - Blue
- `#7F3F98` - Purple
- `#D93A49` - Red
- `#057839` - Green

## Topic Types

- `public` - Public topics
- `private` - Private topics
- `direct` - Direct messages

## Entity Status

- `active` - Active entities
- `completed` - Completed entities
- `archived` - Archived entities

## Triggers

- **Message Created** - Fired when a new message is sent
- **Entity Created** - Fired when a new entity is created

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.created":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "entity.created":
        entity = result["entity"]
        print(f"New entity: {entity.title}")
```

## Language Support

Jandi is a Korean platform, but the API supports international content:

```python
# Korean message
await client.send_message(
    topic_id=topic_id,
    body="안녕하세요! 반갑습니다."
)

# English message
await client.send_message(
    topic_id=topic_id,
    body="Hello! Nice to meet you."
)
```

## Documentation

- Jandi Platform: https://lp.yoom.fun/apps/jandi
- API Base URL: `https://api.jandi.com/connect`

## Error Handling

```python
try:
    message_id = await client.send_message(
        topic_id=topic_id,
        body="안녕하세요"
    )
except Exception as e:
    print(f"Error: {e}")
```