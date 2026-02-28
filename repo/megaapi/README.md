# MEGA API 클라이언트

MEGA API를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 MEGA API에 접근하여 텍스트 메시지 전송 및 삭제 기능을 제공합니다.

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

1. MEGA 개발자 포털 접속
2. 앱 생성 및 API 키 발급
3. 발급된 API 키 저장

## 사용법

### 초기화

```python
from megaapi import MegaapiClient

client = MegaapiClient(
    api_key="YOUR_API_KEY"
)
```

### 예시 코드

```python
# 텍스트 메시지 전송
result = client.send_text_message(
    chat_id="chat123",
    text="Hello from MEGA API!"
)
print(result)

# 리플라이 메시지 전송
result = client.send_text_message(
    chat_id="chat123",
    text="This is a reply",
    reply_to_message_id="msg456"
)

# 메시지 삭제 (발신자만)
result = client.delete_message(
    chat_id="chat123",
    message_id="msg456",
    for_all_users=False
)

# 메시지 삭제 (모든 사용자)
result = client.delete_message(
    chat_id="chat123",
    message_id="msg789",
    for_all_users=True
)
```

## API 액션

- `send_text_message` - Send Text Message
- `delete_message` - Delete Message

## 액션 파라미터

### send_text_message
- `chat_id` (string, required) - 채팅 ID 또는 사용자 ID
- `text` (string, required) - 전송할 메시지 내용
- `reply_to_message_id` (string, optional) - 리플라이할 메시지 ID

### delete_message
- `chat_id` (string, required) - 채팅 ID
- `message_id` (string, required) - 삭제할 메시지 ID
- `for_all_users` (boolean, optional) - 모든 사용자에 대해 삭제 여부 (기본값: false)

## 에러 처리

```python
try:
    result = client.send_text_message("chat123", "Hello!")
except ValueError as e:
    print("Validation error:", str(e))
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청에 대한 레이트 리밋이 적용될 수 있습니다.

## 라이선스

MIT License