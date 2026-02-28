# Reamaze SDK

Reamaze는 고객관계 관리 및 지원 티켓 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Reamaze 웹사이트](https://www.reamaze.com)에 접속하여 계정을 생성합니다.
2. Settings > API & Webhooks 메뉴로 이동합니다.
3. 'Generate API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키와 계정 브랜드 이름을 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from reamaze import ReamazeClient

client = ReamazeClient(
    api_key="your_api_key_here",
    account="your_brand_name",
    base_url="https://api.reamaze.com"
)
```

### 대화(티켓) 생성

```python
conversation = client.create_conversation(
    subject="주문 관련 문의",
    message주문 번호 #12345의 배송 상태를 확인하고 싶습니다.",
    customer_email="customer@example.com",
    customer_name="홍길동",
    channel="email",
    tags=["주문", "배송"],
    user_assignee="support@example.com"
)

print(f"대화 ID: {conversation['conversation']['slug']}")
```

### 대화 목록 조회

```python
conversations = client.list_conversations(
    status="open",
    channel="email",
    limit=20,
    page=1
)

for conv in conversations:
    print(f"{conv['slug']}: {conv['subject']} ({conv['status']})")
```

### 대화 업데이트

```python
updated = client.update_conversation(
    conversation_id="conversation-slug",
    status="resolved",
    user_assignee="agent@example.com"
)
```

### 메시지 추가

```python
message = client.add_message(
    conversation_id="conversation-slug",
    body고객님, 배송이 도착했습니다. 확인 부탁드립니다.",
    internal=False
)

print(f"메시지 ID: {message['message']['id']}")
```

### 고객 생성

```python
customer = client.create_customer(
    email="newcustomer@example.com",
    name="김철수",
    phone="010-1234-5678",
    company="ABC Corp",
    location="서울",
    metadata={
        "tier": "gold",
        "signup_date": "2024-01-01"
    }
)

print(f"고객 ID: {customer['customer']['id']}")
```

### 고객 목록 조회

```python
customers = client.list_customers(
    search="ABC Corp",
    limit=50,
    page=1
)

for customer in customers:
    print(f"{customer['email']}: {customer['name']}")
```

### 직원 목록 조회

```python
users = client.list_users()

for user in users:
    print(f"{user['name']}: {user['email']}")
```

### 통계 조회

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 대화: {stats['totalConversations']}")
print(f"해결된 대화: {stats['resolvedConversations']}")
print(f"평균 응답 시간: {stats['avgResponseTime']}분")
```

### 도움말 문서 생성

```python
article = client.create_article(
    title="주문 취소 방법",
    content="<h1>주문 취소 방법</h1><p>다음 단계를 따르세요...</p>",
    category_id="category_123",
    published=True
)

print(f"문서 ID: {article['article']['id']}")
```

### 채널 목록 조회

```python
channels = client.list_channels()

for channel in channels:
    print(f"{channel['name']}: {channel['type']}")
```

## 기능

- ✅ 대화(티켓) 관리
- ✅ 메시지 관리
- ✅ 고객 관리
- ✅ 직원 관리
- ✅ 통계 및 분석
- ✅ 도움말 문서 관리
- ✅ 멀티채널 지원 (이메일, 채팅, 소셜)

## 라이선스

MIT License