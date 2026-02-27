# BigMailer API Integration

BigMailer의 REST API를 사용하여 연락처(Contact)를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from big_mailer import BigMailerClient

client = BigMailerClient(api_key="your_api_key_here")
```

### 연락처 관리

```python
# 연락처 생성
contact = client.create_contact(
    email="user@example.com",
    brand_id="brand_123",
    list_ids=["list_001", "list_002"],
    field_values={
        "first_name": "John",
        "last_name": "Doe"
    },
    tags=["vip", "newsletter"],
    opt_in=True
)

# 연락처 조회
contact = client.get_contact(contact_id="contact_id", brand_id="brand_123")

# 연락처 업데이트
updated = client.update_contact(
    contact_id="contact_id",
    brand_id="brand_123",
    field_values={"phone": "555-1234"}
)

# 연락처 삭제
client.delete_contact(contact_id="contact_id", brand_id="brand_123")

# 연락처 목록
contacts = client.list_contacts(
    brand_id="brand_123",
    limit=100,
    offset=0
)

# 필드 목록 조회
fields = client.list_fields(brand_id="brand_123")
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/contacts` | POST | 연락처 생성 |
| `/contacts/{id}` | GET | 연락처 조회 |
| `/contacts/{id}` | PUT | 연락처 업데이트 |
| `/contacts/{id}` | DELETE | 연락처 삭제 |
| `/contacts` | GET | 연락처 목록 |
| `/fields` | GET | 필드 목록 |

## 예외 처리

```python
from big_mailer import BigMailerClient, BigMailerAPIError, BigMailerAuthError

try:
    contact = client.create_contact(email="user@example.com", brand_id="brand_123")
except BigMailerAuthError as e:
    print("인증 오류:", e)
except BigMailerAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `create_contact()` | 새 연락처 생성 |
| `get_contact()` | 연락처 조회 |
| `update_contact()` | 연락처 업데이트 |
| `delete_contact()` | 연락처 삭제 |
| `list_contacts()` | 연락처 목록 |
| `list_fields()` | 사용자 정의 필드 목록 |

## API 참조

- [BigMailer API Documentation](https://bigmailer.io/docs/api/)