# BotStar API Integration

BotStar 챗봇 플랫폼의 API를 사용하여 엔티티(Entity)를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from botstar import BotStarClient

client = BotStarClient(
    access_token="your_access_token_here",
    namespace_id="your_namespace_id"  # Optional
)
```

### 엔티티 관리

```python
# 엔티티 생성
entity = client.create_entity_item(
    entity_type="user",
    entity_id="user_123",
    variables={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    },
    metadata={"source": "website"}
)

# 엔티티 조회
entity = client.get_entity_item(
    entity_type="user",
    entity_id="user_123"
)

# 엔티티 업데이트
updated = client.update_entity_item(
    entity_type="user",
    entity_id="user_123",
    variables={"phone": "+9876543210"}
)

# 엔티티 삭제
client.delete_entity_item(
    entity_type="user",
    entity_id="user_123"
)

# 엔티티 검색
entities = client.search_entity_items(
    entity_type="user",
    filter_conditions={"status": "active"},
    limit=100,
    offset=0
)
```

### 메시지 브로드캐스트

```python
# 모든 사용자에게 메시지 전송
result = client.broadcast_message(
    message="Hello everyone!",
    channel="messenger"
)

# 특정 사용자들에게 전송
result = client.broadcast_message(
    message="Welcome!",
    channel="messenger",
    target_users=["user_1", "user_2", "user_3"]
)
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/entity` | POST | 엔티티 생성/업데이트 |
| `/entity` | GET | 엔티티 조회 |
| `/entity` | DELETE | 엔티티 삭제 |
| `/entities` | GET | 엔티티 검색 |
| `/broadcast` | POST | 메시지 브로드캐스트 |

## 예외 처리

```python
from botstar import BotStarClient, BotStarAPIError, BotStarAuthError

try:
    entity = client.create_entity_item(
        entity_type="user",
        entity_id="user_123",
        variables={"name": "John"}
    )
except BotStarAuthError as e:
    print("인증 오류:", e)
except BotStarAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `create_entity_item()` | 엔티티 생성 |
| `get_entity_item()` | 엔티티 조회 |
| `update_entity_item()` | 엔티티 업데이트 |
| `delete_entity_item()` | 엔티티 삭제 |
| `search_entity_items()` | 엔티티 검색 |
| `broadcast_message()` | 메시지 브로드캐스트 |

## API 참조

- [BotStar API Documentation](https://docs.botstar.com/api/)