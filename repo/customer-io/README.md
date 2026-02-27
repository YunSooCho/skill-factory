# Customer.io API Client

Customer.io용 Python 클라이언트 - 고객 참여 및 자동화 플랫폼

## 설치

```bash
pip install -r requirements.txt
```

## API Credentials 획득

1. [Customer.io 계정 생성](https://customer.io/)
2. 로그인 후 Settings > Integrations > API Credentials 접근
3. Site ID와 API Key 획득
4. 리전 확인 (US 또는 EU)

## 사용법

### 클라이언트 초기화

```python
from customer_io_client import create_customerio_client

client = create_customerio_client(
    site_id='your-site-id',
    api_key='your-api-key',
    region='us'  # 'us' 또는 'eu'
)
```

### 고객 생성

```python
customer = client.create_customer(
    id='customer_123',
    email='user@example.com',
    name='John Doe',
    attributes={
        'plan': 'premium',
        'signup_date': '2024-01-15',
        'country': 'Japan'
    },
    created_at='1705276800'  # Unix timestamp (선택)
)

print(f"Customer ID: {customer.get('id')}")
```

### 고객 업데이트

```python
client.update_customer(
    id='customer_123',
    email='new-email@example.com',
    attributes={'plan': 'enterprise', 'last_login': '2024-02-28'}
)
```

### 고객 삭제

```python
client.delete_customer(id='customer_123')
```

### 고객 이벤트 추적

```python
client.track_customer_event(
    customer_id='customer_123',
    name='purchase_completed',
    data={
        'amount': 99.99,
        'product': 'Premium Plan',
        'transaction_id': 'TXN-12345'
    },
    timestamp=1709164800  # Unix timestamp (선택)
)
```

### 익명 이벤트 추적

```python
client.track_anonymous_event(
    name='page_viewed',
    data={
        'page': '/pricing',
        'referrer': 'google.com',
        'duration': 45
    }
)
```

### 수동 세그먼트에 고객 추가

```python
client.add_customer_to_segment(
    customer_id='customer_123',
    segment_id=1
)
```

### 수동 세그먼트에서 고객 삭제

```python
client.remove_customer_from_segment(
    customer_id='customer_123',
    segment_id=1
)
```

### 고객 목록 조회

```python
customers = client.list_customers(
    limit=50,
    start='customer_100',
    email='user@example.com'  # 선택: 이메일로 필터링
)

for customer in customers:
    print(f"{customer['email']}: {customer['name']}")
```

### 고객 활동 내역 조회

```python
activities = client.get_customer_activities(
    customer_id='customer_123',
    limit=20,
    type='email_click'  # email_actioned, email_opened, email_clicked, etc.
)

for activity in activities:
    print(f"{activity['type']}: {activity['timestamp']}")
```

### 폼 제출

```python
client.submit_form(
    form_id=1,
    customer_id='customer_123',
    data={
        'name': 'John Doe',
        'message': 'I love your product!',
        'rating': 5
    }
)
```

## Track API vs Management API

Customer.io는 두 개의 API를 제공합니다:

1. **Management API** (`/v1`): 고객 데이터 관리
2. **Track API** (`/track/v1`): 이벤트 및 익명 활동 추적

이 클라이언트는 두 API를 자동으로 처리합니다.

## 리전 설정

- **US 리전**: 기본값, `https://api.customer.io` 및 `https://track.customer.io`
- **EU 리전**: `https://api-eu.customer.io` 및 `https://track-eu.customer.io`

```python
client = create_customerio_client(
    site_id='your-site-id',
    api_key='your-api-key',
    region='eu'  # EU 리전 사용
)
```

## 주요 기능

1. **고객 관리**: 생성, 업데이트, 삭제, 조회
2. **이벤트 추적**: 고객 및 익명 이벤트
3. **세그먼트 관리**: 수동 세그먼트 조작
4. **활동 내역**: 고객 활동 기록 조회
5. **폼 제출**: 웹폼 데이터 수집

## 에러 처리

```python
from customer_io_client import CustomerIOError, RateLimitError

try:
    customer = client.create_customer(
        id='customer_123',
        email='user@example.com'
    )
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry: {e}")
except CustomerIOError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 60 요청
- Rate limit 초과 시 `Retry-After` 헤더 반환
- 무료 요금제: 월 400 고객
- 유료 요금제: 무제한

## 모범 사례

1. **이메일 필수**: 이메일은 식별자로 사용됩니다
2. **속성 정규화**: 커스텀 속성에 underscore 사용 (`last_login`)
3. **일관된 이벤트 이름**: 이벤트 이름에 snake_case 사용
4. **Rate Limiting**: 클라이언트가 자동 처리하므로 걱정 없음

## 지원

자세한 API 문서: [Customer.io API Documentation](https://customer.io/docs/api/)