# BoNow API Integration

BoNow 마케팅 자동화 플랫폼의 API를 사용하여 리드(Lead)를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from bownow import BoNowClient

client = BoNowClient(
    api_key="your_api_key_here",
    secret_token="your_secret_token"  # Optional
)
```

### 리드 관리

```python
# 리드 생성
lead = client.create_lead(
    email="user@example.com",
    name="John Doe",
    company="Example Inc",
    phone="+81-1234-5678",
    status="new",
    tags=["newsletter", "vip"],
    custom_fields={
        "source": "website",
        "score": 85
    },
    memo="Website inquiry"
)

# 리드 조회
lead = client.get_lead(lead_id="lead_id_here")

# 리드 검색
leads = client.search_leads(
    email="user@example.com",
    status="active",
    limit=20
)

# 회사별 검색
leads = client.search_leads(
    company="Example Inc",
    limit=50
)

# 리드 업데이트
updated = client.update_lead(
    lead_id="lead_id_here",
    status="contacted",
    phone="+81-9876-5432",
    tags=["newsletter", "vip", "contacted"]
)

# 리드 삭제
client.delete_lead(lead_id="lead_id_here")
```

### 태그 관리

```python
# 태그 추가
client.add_tags_to_lead(
    lead_id="lead_id_here",
    tags=["premium", "high-priority"]
)

# 태그 제거
client.remove_tags_from_lead(
    lead_id="lead_id_here",
    tags=["newsletter"]
)
```

### 상태 관리

```python
# 사용 가능한 상태 목록 조회
statuses = client.get_statuses()
for status in statuses:
    print(f"{status['id']}: {status['name']}")
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/leads` | POST | 리드 생성 |
| `/leads/{id}` | GET | 리드 조회 |
| `/leads/{id}` | PUT | 리드 업데이트 |
| `/leads/{id}` | DELETE | 리드 삭제 |
| `/leads` | GET | 리드 검색 |
| `/leads/{id}/tags` | POST | 태그 추가/제거 |
| `/statuses` | GET | 상태 목록 |

## 예외 처리

```python
from bownow import BoNowClient, BoNowAPIError, BoNowAuthError, BoNowRateLimitError

try:
    lead = client.create_lead(
        email="user@example.com",
        name="John Doe"
    )
except BoNowAuthError as e:
    print("인증 오류:", e)
except BoNowRateLimitError as e:
    print("요청 한도 초과:", e)
except BoNowAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `create_lead()` | 새 리드 생성 |
| `get_lead()` | 리드 조회 |
| `search_leads()` | 리드 검색 |
| `update_lead()` | 리드 업데이트 |
| `delete_lead()` | 리드 삭제 |
| `add_tags_to_lead()` | 태그 추가 |
| `remove_tags_from_lead()` | 태그 제거 |
| `get_statuses()` | 상태 목록 |

## Webhook

BoNow는 다음 Webhook 이벤트를 지원합니다:

1. **리드 업데이트 알림** - 리드 정보가 업데이트될 때
2. **폼 전환 알림** - 웹폼에서 리드가 생성될 때

Webhook을 설정하려면 BoNow 관리 화면에서 Webhook URL을 등록하세요.

## API 참조

- [BoNow API Documentation](https://support.bownow.jp/api/)