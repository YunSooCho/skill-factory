# Benchmark Email API Integration

Benchmark Email의 REST API를 사용하여 연락처(Contact)를 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from benchmark_email import BenchmarkEmailClient

client = BenchmarkEmailClient(api_key="your_api_key_here")
```

### 연락처 관리

```python
# 연락처 추가
contact = client.add_contact(
    email="user@example.com",
    list_id="12345",
    first_name="John",
    last_name="Doe",
    company="Example Inc",
    phone="555-1234",
    custom_fields={
        "source": "website",
        "interest": "marketing"
    },
    double_optin=True
)

# 연락처 검색
contacts = client.search_contact(
    email="user@example.com",
    first_name="John"
)

# 연락처 업데이트
updated = client.update_contact(
    contact_id="contact_id_here",
    first_name="Jane",
    company="New Company"
)

# 연락처 삭제
client.delete_contact(contact_id="contact_id_here")

# 연락처 목록
contacts = client.list_contacts(
    list_id="12345",
    limit=100,
    offset=0
)
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/Contact` | POST | 연락처 추가 |
| `/Contact/Search` | GET | 연락처 검색 |
| `/Contact/Update` | PUT | 연락처 업데이트 |
| `/Contact/Delete` | DELETE | 연락처 삭제 |
| `/Contact/List` | GET | 연락처 목록 |

## 예외 처리

```python
from benchmark_email import BenchmarkEmailClient, BenchmarkEmailAPIError, BenchmarkEmailAuthError

try:
    contact = client.add_contact(email="user@example.com")
except BenchmarkEmailAuthError as e:
    print("인증 오류:", e)
except BenchmarkEmailAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `add_contact()` | 새 연락처 추가 |
| `search_contact()` | 연락처 검색 |
| `update_contact()` | 연락처 정보 업데이트 |
| `delete_contact()` | 연락처 삭제 |
| `list_contacts()` | 연락처 목록 |

## 파라미터

### add_contact()

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| email | str | ✅ | 연락처 이메일 |
| list_id | str | ❌ | 리스트 ID |
| first_name | str | ❌ | 이름 |
| last_name | str | ❌ | 성 |
| company | str | ❌ | 회사 |
| address | str | ❌ | 주소 |
| city | str | ❌ | 도시 |
| state | str | ❌ | 주/도 |
| zip_code | str | ❌ | 우편번호 |
| country | str | ❌ | 국가 |
| phone | str | ❌ | 전화번호 |
| mobile | str | ❌ | 휴대폰 번호 |
| fax | str | ❌ | 팩스 번호 |
| custom_fields | dict | ❌ | 사용자 정의 필드 |
| double_optin | bool | ❌ | 더블 옵인 사용 여부 |

## API 참조

- [Benchmark Email API Documentation](https://www.benchmarkemail.com/API/)