# AskHandle SDK

AskHandle는 고객 문의 및 요청 관리를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [AskHandle 웹사이트](https://askhandle.com)에 접속하여 계정을 생성합니다.
2. 대시보드에서 Settings > API Keys 메뉴로 이동합니다.
3. 'Create API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from askhandle import AskHandleClient

client = AskHandleClient(
    api_key="your_api_key_here",
    base_url="https://api.askhandle.com/v1"
)
```

### 티켓 생성

```python
ticket = client.create_ticket(
    title="로그인 문제",
    description="사용자가 로그인할 수 없음",
    requester_name="홍길동",
    requester_email="hong@example.com",
    priority="high",
    category="로그인",
    tags=["긴급", "버그"]
)

print(f"티켓 ID: {ticket['id']}")
```

### 티켓 목록 조회

```python
tickets = client.list_tickets(
    status="open",
    priority="high",
    limit=20
)

for ticket in tickets:
    print(f"{ticket['id']}: {ticket['title']} ({ticket['status']})")
```

### 티켓 업데이트

```python
updated_ticket = client.update_ticket(
    ticket_id="ticket_123",
    status="in_progress",
    assignee_id="agent_456"
)
```

### 댓글 추가

```python
comment = client.add_comment(
    ticket_id="ticket_123",
    comment="문제를 조사 중입니다. 잠시만 기다려 주세요.",
    author_name="담당자",
    author_email="support@example.com"
)
```

### 고객 생성

```python
customer = client.create_customer(
    name="김철수",
    email="cheolsu@example.com",
    phone="010-1234-5678",
    company="ABC Corp"
)
```

### 통계 조회

```python
stats = client.get_statistics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"총 티켓: {stats['total_tickets']}")
print(f"해결된 티켓: {stats['resolved_tickets']}")
```

## 기능

- ✅ 티켓 생성, 조회, 업데이트
- ✅ 댓글 추가 및 조회
- ✅ 고객 관리
- ✅ 통계 및 리포트
- ✅ 우선순위 및 상태 관리

## 라이선스

MIT License