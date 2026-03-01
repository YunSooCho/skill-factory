# Sleekflow SDK

Sleekflow는 채팅 및 고객지원 워크플로우 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Sleekflow 웹사이트](https://sleekflow.io)에 접속하여 계정을 생성합니다.
2. 대시보드에서 Settings > API Keys 메뉴로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키와 Workspace ID를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from sleekflow import SleekflowClient

client = SleekflowClient(
    api_key="your_api_key_here",
    workspace_id="your_workspace_id",
    base_url="https://api.sleekflow.io/v1"
)
```

### 채팅 세션 생성

```python
session = client.create_chat_session(
    customer_id="customer_123",
    channel="web",
    metadata={
        "source": "homepage",
        "referrer": "google.com"
    }
)

print(f"세션 ID: {session['id']}")
```

### 메시지 전송

```python
message = client.send_message(
    session_id="session_123",
    text="안녕하세요! 무엇을 도와드릴까요?",
    sender_type="agent",
    message_type="text"
)

print(f"메시지 ID: {message['id']}")
```

### 메시지 내역 조회

```python
messages = client.get_messages(
    session_id="session_123",
    limit=50
)

for msg in messages:
    print(f"{msg['senderType']}: {msg['text']}")
```

### 워크플로우 생성

```python
workflow = client.create_workflow(
    name="신규 고객 온보딩",
    description="신규 가입 고객에게 환영 메시지와 가이드 전송",
    steps=[
        {
            "type": "send_message",
            "delay": 0,
            "templateId": "welcome_template"
        },
        {
            "type": "wait",
            "delay": 3600,
            "duration": "1h"
        },
        {
            "type": "send_message",
            "delay": 0,
            "templateId": "guide_template"
        }
    ],
    trigger_type="event",
    is_active=True
)

print(f"워크플로우 ID: {workflow['id']}")
```

### 워크플로우 트리거

```python
result = client.trigger_workflow(
    workflow_id="workflow_123",
    customer_id="customer_456",
    parameters={
        "name": "김철수",
        "product": "Premium"
    }
)

print(f"워크플로우 실행: {result['success']}")
```

### 템플릿 생성

```python
template = client.create_template(
    name="환영 메시지",
    category="greeting",
    content="안녕하세요, {name}님! 서비스에 오신 것을 환영합니다.",
    variables=["name"],
    language="ko"
)

print(f"템플릿 ID: {template['id']}")
```

### AI 챗봇 생성

```python
bot = client.create_bot(
    name="고객지원 봇",
    description="기본적인 고객 질문에 응답하는 AI 봇",
    greeting_message="안녕하세요! 저는 AI 어시스턴트입니다. 무엇을 도와드릴까요?",
    ai_model="gpt-4",
    knowledge_base="kb_123"
)

print(f"봇 ID: {bot['id']}")
```

### 봇 목록 조회

```python
bots = client.list_bots()

for bot in bots:
    print(f"{bot['name']} ({bot['aiModel']}) - {bot['status']}")
```

### 채팅 세션 목록 조회

```python
sessions = client.list_chat_sessions(
    customer_id="customer_123",
    status="active",
    limit=20
)

for session in sessions:
    print(f"{session['id']}: {session['channel']} - {session['status']}")
```

### 분석 데이터 조회

```python
analytics = client.get_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metric="messages",
    channel="web"
)

print(f"총 메시지: {analytics['totalMessages']}")
print(f"평균 응답 시간: {analytics['avgResponseTime']}초")
```

### 고객 이벤트 추적

```python
client.track_customer_event(
    customer_id="customer_123",
    event_name="product_purchased",
    properties={
        "product_id": "prod_456",
        "price": 99900,
        "category": "electronics"
    }
)
```

## 기능

- ✅ 채팅 세션 관리
- ✅ 메시지 전송 및 조회
- ✅ 워크플로우 자동화
- ✅ 메시지 템플릿
- ✅ AI 챗봇 통합
- ✅ 고객 이벤트 추적
- ✅ 분석 및 리포트
- ✅ 멀티채널 지원

## 지원 채널

- 웹사이트 채팅
- WhatsApp
- Facebook Messenger
- Telegram
- Line

## 라이선스

MIT License