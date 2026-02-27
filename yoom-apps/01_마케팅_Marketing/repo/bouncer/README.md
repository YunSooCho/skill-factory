# Bouncer API Integration

Bouncer 이메일 검증 API를 사용하여 이메일 주소의 유효성을 확인하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from bouncer import BouncerClient

client = BouncerClient(api_key="your_api_key_here")
```

### 이메일 검증

```python
# 단일 이메일 검증
result = client.verify_email("user@example.com")
print(f"Status: {result['status']}")  # deliverable, undeliverable, risky, unknown
print(f"Mailbox exists: {result['mailbox_exists']}")
print(f"Is disposable: {result['is_disposable']}")
print(f"Is free email: {result['is_free']}")

# 타임아웃 설정
result = client.verify_email(
    "user@example.com",
    timeout=10
)

# 재시도 설정
result = client.verify_email(
    "user@example.com",
    retry_count=3
)
```

### 대량 이메일 검증

```python
emails = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
]

results = client.verify_emails(emails)
for result in results:
    print(f"{result['email']}: {result['status']}")
```

### 도메인 검증

```python
# 도메인의 이메일 인프라 검증
result = client.verify_domain("example.com")
print(f"MX Valid: {result['mx_valid']}")
print(f"SPF Valid: {result['spf_valid']}")
print(f"DMARC Valid: {result['dmarc_valid']}")
print(f"DMARC Policy: {result['dmarc_policy']}")
```

### 편의 메서드

```python
# 배달 가능 여부 확인
if client.is_deliverable("user@example.com"):
    print("이메일이 유효합니다")

# 리스크 확인
if client.is_risky("user@example.com"):
    print("이메일이 리스크가 있습니다")

# 배달 불가 확인
if client.is_undeliverable("user@example.com"):
    print("이메일이 배달 불가합니다")
```

### 계정 정보

```python
# 남은 크레딧 확인
credits = client.get_credits()
print(f"Remaining credits: {credits['credits']}")

# 계정 정보
account = client.get_account_info()
print(f"Plan: {account['plan']}")
```

## 검증 상태

| 상태 | 설명 |
|------|------|
| `deliverable` | 이메일이 유효하고 배달 가능 |
| `undeliverable` | 이메일이 유효하지 않거나 배달 불가 |
| `risky` | 이메일이 일부 리스크가 있음 |
| `unknown` | 상태 확인 불가 |

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/email/verify` | POST | 이메일 검증 |
| `/email/verify/batch` | POST | 대량 이메일 검증 |
| `/domain/verify` | POST | 도메인 검증 |
| `/account/credits` | GET | 크레딧 확인 |
| `/account` | GET | 계정 정보 |

## 예외 처리

```python
from bouncer import BouncerClient, BouncerAPIError, BouncerAuthError, BouncerRateLimitError

try:
    result = client.verify_email("user@example.com")
except BouncerAuthError as e:
    print("인증 오류:", e)
except BouncerRateLimitError as e:
    print("요청 한도 초과:", e)
except BouncerAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `verify_email()` | 단일 이메일 검증 |
| `verify_emails()` | 대량 이메일 검증 |
| `verify_domain()` | 도메인 검증 |
| `get_credits()` | 크레딧 확인 |
| `get_account_info()` | 계정 정보 |
| `is_deliverable()` | 배달 가능 여부 |
| `is_risky()` | 리스크 여부 |
| `is_undeliverable()` | 배달 불가 여부 |

## API 참조

- [Bouncer API Documentation](https://api.usebouncer.com/)