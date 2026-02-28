# Noor API 클라이언트

Noor API를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Noor API에 접근하여 멤버 목록 조회 및 메시지 게시 기능을 제공합니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. Noor 개발자 포털 접속
2. 앱 생성 및 API 키 발급
3. 발급된 API 키 저장

## 사용법

### 초기화

```python
from noor import NoorClient

client = NoorClient(
    api_key="YOUR_API_KEY"
)
```

### 예시 코드

```python
# 전체 멤버 목록 조회
members = client.get_members(limit=20)
print(members)

# 특정 그룹의 멤버 조회
group_members = client.get_members(group_id="group123", limit=10)
print(group_members)

# 간단한 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="Hello from Noor API!"
)
print(result)

# 멘션이 포함된 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="Hello @user1 and @user2!",
    mention_user_ids=["user1", "user2"]
)

# 리플라이 메시지 게시
result = client.post_message(
    chat_id="chat123",
    text="This is a reply",
    reply_to_message_id="msg456"
)
```

## API 액션

- `get_members` - Get Members
- `post_message` - Post Message

## 액션 파라미터

### get_members
- `group_id` (string, optional) - 그룹 ID (필터링용)
- `limit` (integer, optional) - 반환할 결과 수 (기본값: 50)
- `offset` (integer, optional) - 페이지네이션 오프셋 (기본값: 0)

### post_message
- `chat_id` (string, required) - 채팅 ID
- `text` (string, required) - 게시할 메시지 내용
- `mention_user_ids` (array of strings, optional) - 멘션할 사용자 ID 리스트
- `reply_to_message_id` (string, optional) - 리플라이할 메시지 ID

## 에러 처리

```python
try:
    result = client.post_message("chat123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청에 대한 레이트 리밋이 적용될 수 있습니다.

## 라이선스

MIT License