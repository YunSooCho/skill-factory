# Superchat SDK

Superchat은 라이브채팅 및 고객지원 서비스를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Superchat 웹사이트](https://superchat.com)에 접속하여 계정을 생성합니다.
2. 대시보드에서 Settings > API Keys 메뉴로 이동합니다.
3. 'Generate API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키와 Account ID를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from superchat import SuperchatClient

client = SuperchatClient(
    api_key="your_api_key_here",
    account_id="your_account_id",
    base_url="https://api.superchat.com/v1"
)
```

### 채팅 시작

```python
chat = client.start_chat(
    customer_name="김철수",
    customer_email="cheolsu@example.com",
    initial_message="안녕하세요, 상품 문의가 있습니다.",
    channel="web",
    metadata={
        "page": "/products",
        "referrer": "google.com"
    }
)

print(f"채팅 ID: {chat['id']}")
```

### 메시지 전송

```python
message = client.send_message(
    chat_id="chat_123",
    message안녕하세요! 어떤 상품에 대해 문의하시나요?",
    sender_type="agent",
    message_type="text"
)

print(f"메시지 ID: {message['id']}")
```

### 메시지 내역 조회

```python
messages = client.get_messages(
    chat_id="chat_123",
    limit=50
)

for msg in messages:
    print(f"{msg['senderType']} ({msg['createdAt']}): {msg['message']}")
```

### 채팅 목록 조회

```python
chats = client.list_chats(
    status="active",
    assigned_to="agent_456",
    limit=20
)

for chat in chats:
    print(f"{chat['id']}: {chat['customerName']} - {chat['status']}")
```

### 채팅 업데이트

```python
updated = client.update_chat(
    chat_id="chat_123",
    status="closed",
    tags=["해결완료", "제품문의"]
)
```

### 채팅 종료

```python
result = client.close_chat(chat_id="chat_123")
print(f"채팅 종료: {result['success']}")
```

### 채팅 담당자 지정

```python
result = client.assign_chat(
    chat_id="chat_123",
    agent_id="agent_456"
)

print(f"담당자 지정: {result['success']}")
```

### 고객 생성

```python
customer = client.create_customer(
    name="이영희",
    email="younghee@example.com",
    phone="010-9876-5432",
    company="XYZ Corp",
    custom_attributes={
        "tier": "VIP",
        "signup_date": "2024-01-15"
    }
)

print(f"고객 ID: {customer['id']}")
```

### 고객 정보 업데이트

```python
updated = client.update_customer(
    customer_id="customer_789",
    name="이영희 (수정)",
    custom_attributes={
        "tier": "premium"
    }
)
```

### AI 챗봇 생성

```python
bot = client.create_bot(
    name="고객지원 어시스턴트",
    welcome_message="안녕하세요! 무엇을 도와드릴까요?",
    handoff_message="잡시만 기다려 주시면 상담원이 연결됩니다.",
    ai_provider="openai",
    ai_model="gpt-4o-mini",
    knowledge_base="kb_123",
    is_active=True
)

print(f"봇 ID: {bot['id']}")
```

### 봇 목록 조회

```python
bots = client.list_bots()

for bot in bots:
    print(f"{bot['name']} ({bot['aiModel']}) - {bot['status']}")
```

### 봇 업데이트

```python
updated = client.update_bot(
    bot_id="bot_456",
    welcome_message="반갑습니다! 무엇을 도와드릴까요?",
    is_active=True
)
```

### 템플릿 응답 생성

```python
canned = client.create_canned_response(
    title="영업시간 안내",
    content="저희 영업시간은 평일 09:00~18:00입니다. 문의하신 내용은 영업시간 내에 답변드리겠습니다.",
    shortcuts=["영업시간", "운영시간"],
    category="공통"
)

print(f"템플릿 ID: {canned['id']}")
```

### 템플릿 응답 목록 조회

```python
responses = client.list_canned_responses(
    category="공통",
    limit=20
)

for resp in responses:
    print(f"{resp['title']}: {resp['content']}")
```

### 에이전트 목록 조회

```python
agents = client.list_agents()

for agent in agents:
    print(f"{agent['name']} - {agent['status']} ({agent['role']})")
```

### 분석 데이터 조회

```python
analytics = client.get_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metric="all"
)

print(f"총 채팅: {analytics['totalChats']}")
print(f"총 메시지: {analytics['totalMessages']}")
print(f"평균 응답 시간: {analytics['avgResponseTime']}초")
print(f"고객 만족도: {analytics['satisfactionScore']}")
```

## 채팅 상태

- **active**: 활성
- **closed**: 종료
- **archived**: 보관

## 발신자 타입

- **agent**: 에이전트
- **customer**: 고객
- **bot**: 봇
- **system**: 시스템

## 메시지 타입

- **text**: 텍스트
- **image**: 이미지
- **video**: 비디오
- **file**: 파일
- **location**: 위치

## 기능

- ✅ 라이브 채팅 관리
- ✅ 메시지 전송 및 조회
- ✅ 고객 관리
- ✅ AI 챗봇 통합
- ✅ 템플릿 응답
- ✅ 에이전트 관리
- ✅ 담당자 지정
- ✅ 분석 및 리포트

## 지원 채널

- 웹사이트 라이브 채팅
- WhatsApp
- Facebook Messenger
- Telegram
- Line
- SMS

## 라이선스

MIT License