# Relation SDK

Relation은 고객 관계 관리(CRM)를 위한 Python SDK입니다.

## 설치

```bash
pip install -r requirements.txt
```

## API 키 발급 방법

1. [Relation 웹사이트](https://relation.io)에 접속하여 계정을 생성합니다.
2. 대시보드에서 Settings > API Keys 메뉴로 이동합니다.
3. 'Generate API Key' 버튼을 클릭하여 새 API 키를 생성합니다.
4. 생성된 API 키를 안전한 곳에 저장합니다.

## 사용법

### 클라이언트 초기화

```python
from relation import RelationClient

client = RelationClient(
    api_key="your_api_key_here",
    base_url="https://api.relation.io/v1"
)
```

### 연락처 생성

```python
contact = client.create_contact(
    email="customer@example.com",
    first_name="철수",
    last_name="김",
    phone="010-1234-5678",
    company="ABC Corp",
    title="마케팅 매니저",
    tags=["VIP", "대기업"],
    attributes={
        "tier": "gold",
        "signup_date": "2024-01-01"
    }
)

print(f"연락처 ID: {contact['id']}")
```

### 연락처 조회

```python
contact = client.get_contact(contact_id="contact_123")

print(f"{contact['firstName']} {contact['lastName']}")
print(f"회사: {contact['company']}")
print(f"태그: {contact['tags']}")
```

### 연락처 목록 조회

```python
contacts = client.list_contacts(
    tags=["VIP"],
    created_after="2024-01-01",
    limit=20
)

for contact in contacts:
    print(f"{contact['email']}: {contact['firstName']} {contact['lastName']}")
```

### 연락처 업데이트

```python
updated = client.update_contact(
    contact_id="contact_123",
    title="시니어 마케팅 매니저",
    add_tags=["중요고객"],
    remove_tags=["신규"]
)
```

### 세그먼트 생성

```python
segment = client.create_segment(
    name="VIP 고객",
    description="연간 매출 1억 이상 고객",
    criteria={
        "tags": ["VIP"],
        "attributes": {
            "tier": "gold"
        }
    }
)

print(f"세그먼트 ID: {segment['id']}")
```

### 세그먼트 연락처 조회

```python
contacts = client.get_segment_contacts(
    segment_id="segment_456",
    limit=50
)

print(f"VIP 고객 수: {len(contacts)}")
```

### 노트 생성

```python
note = client.create_note(
    contact_id="contact_123",
    content고객과의 통화 결과 - 제품 데모 일정 조율 완료",
    author_id="user_456",
    note_type="call"
)

print(f"노트 ID: {note['id']}")
```

### 태스크 생성

```python
task = client.create_task(
    contact_id="contact_123",
    title="제품 데모 일정 확인",
    description="고객과 협의한 날짜에 데모 진행 예정",
    due_date="2024-02-15",
    assignee_id="user_456",
    priority="high"
)

print(f"태스크 ID: {task['id']}")
```

### 태스크 목록 조회

```python
tasks = client.list_tasks(
    contact_id="contact_123",
    status="pending",
    priority="high",
    limit=10
)

for task in tasks:
    print(f"{task['title']} - {task['dueDate']}")
```

### 이벤트 추적

```python
client.track_event(
    contact_id="contact_123",
    event_name="product_viewed",
    properties={
        "product_id": "prod_789",
        "price": 99900,
        "category": "electronics"
    }
)
```

### 연락처 이벤트 기록 조회

```python
events = client.get_contact_events(
    contact_id="contact_123",
    event_type="product_viewed",
    limit=20
)

for event in events:
    print(f"{event['eventName']}: {event['properties']}")
    print(f"시간: {event['createdAt']}")
```

### 연락처 삭제

```python
result = client.delete_contact(contact_id="contact_123")
print(f"삭제 완료: {result['success']}")
```

## 기능

- ✅ 연락처 관리 (생성, 조회, 업데이트, 삭제)
- ✅ 세그먼트 기반 고객 분류
- ✅ 노트 및 활동 기록
- ✅ 태스크 관리
- ✅ 이벤트 추적
- ✅ 통합 검색

## 라이선스

MIT License