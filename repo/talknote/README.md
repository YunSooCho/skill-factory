# Talknote API 클라이언트

Talknote를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Talknote API에 접근하여 스레드 및 노트에 메시지를 게시하는 기능을 제공합니다.

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

1. Talknote 개발자 포털 접속
2. 앱 생성 및 API 키 발급
3. 발급된 API 키 저장

## 사용법

### 초기화

```python
from talknote import TalknoteClient

client = TalknoteClient(
    api_key="YOUR_API_KEY"
)
```

### 예시 코드

```python
# 스레드에 메시지 게시
result = client.post_message_to_thread(
    thread_id="thread123",
    message="This is a message to the thread."
)
print(result)

# 멘션이 포함된 스레드 메시지 게시
result = client.post_message_to_thread(
    thread_id="thread123",
    message="@user1 Please check this.",
    mention_user_ids=["user1", "user2"]
)

# 노트에 메시지 게시
result = client.post_message_to_note(
    note_id="note456",
    message="This is a message to the note."
)
print(result)

# 멘션이 포함된 노트 메시지 게시
result = client.post_message_to_note(
    note_id="note456",
    message="@team Important update!",
    mention_user_ids=["user1", "user2", "user3"]
)
```

## API 액션

- `post_message_to_thread` - スレッドにメッセージを投稿
- `post_message_to_note` - ノートへメッセージを投稿

## 액션 파라미터

### post_message_to_thread
- `thread_id` (string, required) - 스레드 ID
- `message` (string, required) - 게시할 메시지 내용
- `mention_user_ids` (array of strings, optional) - 멘션할 사용자 ID 리스트

### post_message_to_note
- `note_id` (string, required) - 노트 ID
- `message` (string, required) - 게시할 메시지 내용
- `mention_user_ids` (array of strings, optional) - 멘션할 사용자 ID 리스트

## 에러 처리

```python
try:
    result = client.post_message_to_thread("thread123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청에 대한 레이트 리밋이 적용될 수 있습니다.

## 라이선스

MIT License