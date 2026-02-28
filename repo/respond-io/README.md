# Respond.io SDK

Respond.io는 멀티채널 고객지원을 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Respond.io 웹사이트](https://respond.io)에 접속하여 계정을 생성합니다.
2. Settings > APIs & Webhooks 메뉴로 이동합니다.
3. 'Generate API Token' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from respond_io import RespondIOClient

client = RespondIOClient(
    api_key="your_api_key_here",
    base_url="https://api.respond.io/v1"
)
```

### 메시지 전송

```python
message = client.create_message(
    channel_id="channel_123",
    text="안녕하세요! 무엇을 도와드릴까요?",
    customer_id="customer_456"
)

print(f"메시지 ID: {message['id']}")
```

### 대화 생성

```python
conversation = client.create_conversation(
    customer_id="customer_456",
    channel_id="channel_123",
    initial_message="제품 관련 문의입니다.",
    tags=["문의", "제품"]
)

print(f"대화 ID: {conversation['id']}")
```

### 대화 목록 조회

```python
conversations = client.list_conversations(
    status="open",
    assigned_to="user_789",
    limit=20
)

for conv in conversations:
    print(f"{conv['id']}: {conv['status']} (할당: {conv['assignedTo']})")
```

### 대화 업데이트

```python
updated = client.update_conversation(
    conversation_id="conv_123",
    status="closed",
    assigned_to="user_789"
)
```

### 대화 종료

```python
result = client.close_conversation(conversation_id="conv_123")
print(f"대화 종료 완료: {result['success']}")
```

### 고객 생성

```python
customer = client.create_customer(
    external_id="user_999",
    name="김철수",
    email="cheolsu@example.com",
    phone="010-1234-5678",
    avatar_url="https://example.com/avatar.jpg",
    custom_attributes={
        "tier": "VIP",
        "signup_date": "2024-01-01"
    }
)

print(f"고객 ID: {customer['id']}")
```

### 고객 정보 업데이트

```python
updated = client.update_customer(
    customer_id="customer_456",
    name="김철수 (수정)",
    custom_attributes={
        "tier": "premium"
    }
)
```

### 채널 목록 조회

```python
channels = client.list_channels()

for channel in channels:
    print(f"{channel['name']}: {channel['type']}")
```

### 사용자 목록 조회

```python
users = client.list_users()

for user in users:
    print(f"{user['name']}: {user['role']}")
```

### 대화 담당자 지정

```python
result = client.assign_conversation(
    conversation_id="conv_123",
    user_id="user_789"
)

print(f"담당자 지정 완료: {result['success']}")
```

### 노트 추가

```python
note = client.add_note(
    conversation_id="conv_123",
    content고객이 제품 교환을 요청함 - 배송비는 우리가 부담하기로 확정",
    author_id="user_789"
)

print(f"노트 ID: {note['id']}")
```

### 메시지 내역 조회

```python
messages = client.list_messages(
    conversation_id="conv_123",
    limit=50
)

for msg in messages:
    print(f"{msg['author']} ( {msg['createdAt']}): {msg['text']}")
```

### 통계 조회

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 대화: {stats['totalConversations']}")
print(f"평균 응답 시간: {stats['avgResponseTime']}초")
print(f"해결된 대화: {stats['resolvedConversations']}")
```

## 기능

- ✅ 멀티채널 메시지 관리
- ✅ 대화 생성, 조회, 업데이트, 종료
- ✅ 고객 관리
- ✅ 담당자 지정
- ✅ 노트 추가
- ✅ 채널 및 사용자 관리
- ✅ 통계 및 분석

## 지원 채널

- 웹사이트 라이브 채팅
- WhatsApp
- Facebook Messenger
- Telegram
- Email
- SMS
- Line
- Viber

## 라이선스

MIT License