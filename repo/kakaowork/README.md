# Kakaowork API Client

Python async client for Kakaowork Korean enterprise messaging platform API.

## Features

- Send messages to users
- Build message blocks for rich formatting
- User and department management
- Task management
- Webhook event handling

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Visit [Kakaowork](https://lp.yoom.fun/apps/kakaowork)
2. Sign up or log in to your account (in Korean)
3. Navigate to Settings → API Keys (설정 → API 키)
4. Click "Generate New API Key" (새 API 키 생성)
5. Copy your API key and store it securely
6. Enable necessary permissions

## Usage

```python
import asyncio
from kakaowork.client import KakaoworkClient

async def main():
    api_key = "your_kakaowork_api_key"

    async with KakaoworkClient(api_key) as client:
        # Send a simple text message
        message_id = await client.send_message(
            user_id="user_1234567890",
            content="안녕하세요! 카카오워크 API에서 보낸 메시지입니다."
        )

        # Send a message with blocks (rich formatting)
        message_id = await client.send_message(
            user_id="user_1234567890",
            content="프로젝트 업데이트",
            blocks=[
                {
                    "type": "header",
                    "text": "프로젝트 현황",
                    "style": "blue"
                },
                {
                    "type": "text",
                    "content": "프로젝트가 순조롭게 진행되고 있습니다."
                },
                {
                    "type": "divider"
                },
                {
                    "type": "text",
                    "content": "• 프론트엔드: 완료\n• 백엔드: 진행중\n• 테스트: 대기중"
                }
            ]
        )

        # Get users
        users = await client.get_users(limit=100)
        print(f"Found {len(users)} users")

        # Get departments
        departments = await client.get_departments(limit=50)
        print(f"Found {len(departments)} departments")

        # Get users from specific department
        if departments:
            dept_users = await client.get_users(
                department_id=departments[0].department_id
            )
            print(f"Department users: {len(dept_users)}")

        # Create a task
        task = await client.create_task(
            user_id="user_1234567890",
            title="문서 작성",
            description="프로젝트 문서를 작성해주세요",
            due_date="2024-01-31"
        )

        # Get tasks
        tasks = await client.get_tasks(
            user_id="user_1234567890",
            status="pending",
            limit=20
        )
        print(f"Found {len(tasks)} pending tasks")

asyncio.run(main())
```

## API Actions

1. **Send Message** - Send a message to a user
2. **Get Messages** - Get messages from a conversation
3. **Get Users** - Get users (optionally filtered by department)
4. **Get Departments** - Get departments
5. **Create Task** - Create a task for a user
6. **Get Tasks** - Get tasks (optionally filtered by user and status)

## Message Blocks

Create rich messages with blocks:

```python
blocks = [
    # Header block
    {
        "type": "header",
        "text": "중요 알림",
        "style": "blue"  # blue or yellow
    },
    # Text block
    {
        "type": "text",
        "content": "여기에 텍스트 내용을 입력하세요."
    },
    # Divider block
    {
        "type": "divider"
    },
    # Button block
    {
        "type": "button",
        "text": "자세히 보기",
        "action": {
            "type": "open_url",
            "url": "https://example.com"
        }
    }
]
```

## Task Status

- `pending` - Task is pending
- `in_progress` - Task is in progress
- `completed` - Task is completed
- `cancelled` - Task is cancelled

## Language Support

Kakaowork is a Korean platform, but supports international content:

```python
# Korean message
await client.send_message(
    user_id="user_123",
    content="안녕하세요! 반갑습니다."
)

# English message
await client.send_message(
    user_id="user_123",
    content="Hello! Nice to meet you."
)
```

## Triggers

- **Message Created** - Fired when a new message is sent
- **Task Created** - Fired when a new task is created

## Webhook Handling

```python
def handle_webhook(webhook_data):
    result = client.handle_webhook(webhook_data)

    if result["event_type"] == "message.created":
        message = result["message"]
        print(f"New message: {message.content}")
    elif result["event_type"] == "task.created":
        task = result["task"]
        print(f"New task: {task.title}")
```

## Pagination

Use cursors for pagination:

```python
cursor = None
while True:
    users = await client.get_users(limit=100, cursor=cursor)
    if not users:
        break
    # Process users
    cursor = users[-1].cursor  # Get next cursor
```

## Documentation

- Kakaowork Platform: https://lp.yoom.fun/apps/kakaowork
- API Base URL: `https://api.kakaowork.com/v1/api`

## Error Handling

```python
try:
    message_id = await client.send_message(
        user_id="user_1234567890",
        content="안녕하세요"
    )
except Exception as e:
    print(f"Error: {e}")
```