# Cuenote SMS API Client

Cuenote SMS용 Python 클라이언트 - 일본 SMS 마케팅 서비스

## 설치

```bash
pip install -r requirements.txt
```

## API Credentials 획득

1. [Cuenote 계정 생성](https://www.cuenote.jp/)
2. 로그인后 Settings > API 접근
3. API Key와 API Secret 생성
4. 자격 증명 복사

## 사용법

### 클라이언트 초기화

```python
from cuenote_sms_client import create_cuenote_sms_client

client = create_cuenote_sms_client(
    api_key='your-api-key',
    api_secret='your-api-secret'
)
```

### 주소록 생성

```python
address_book = client.create_address_book(
    name='New Customers',
    description='Customers from January 2024'
)

address_book_id = address_book['addressBookId']
print(f"Address Book ID: {address_book_id}")
```

### 주소록 목록 조회

```python
books = client.list_address_books(limit=20)

for book in books['addressBooks']:
    print(f"{book['name']}: {book['count']} contacts")
```

### 주소록 상세 조회

```python
book = client.get_address_book(address_book_id='book-123')
print(f"Name: {book['name']}")
print(f"Description: {book['description']}")
```

### 주소록 업데이트

```python
client.update_address_book(
    address_book_id='book-123',
    name='Updated Name',
    description='New description'
)
```

### 주소록 삭제

```python
client.delete_address_book(address_book_id='book-123')
```

### 전화번호로 SMS 배포 생성

```python
delivery = client.create_sms_delivery_phone_numbers(
    phone_numbers=['+819012345678', '+819023456789'],
    message='こんにちは！特別オファーをご案内します。',
    scheduled_at='2024-02-28T10:00:00Z',  # 선택: 예약 시간
    track_urls=False  # 선택: URL 추적 사용 여부
)

delivery_id = delivery['deliveryId']
print(f"Delivery ID: {delivery_id}")
print(f"Status: {delivery['status']}")
```

### 주소록을 사용하여 SMS 배포 생성

```python
delivery = client.create_sms_delivery_address_book(
    address_book_id='book-123',
    message='キャンペーン情報をお知らせします。',
    scheduled_at='2024-02-28T10:00:00Z',
    track_urls=True
)
```

### 배포 업데이트 (예약 전에만 가능)

```python
client.update_sms_delivery(
    delivery_id='delivery-123',
    message='修正されたメッセージ',
    scheduled_at='2024-02-28T12:00:00Z'
)
```

### 배포 상세 조회

```python
delivery = client.get_delivery(delivery_id='delivery-123')

print(f"Status: {delivery['status']}")
print(f"Total Recipients: {delivery['totalRecipients']}")
print(f"Sent: {delivery['sentCount']}")
print(f"Delivered: {delivery['deliveredCount']}")
print(f"Failed: {delivery['failedCount']}")
```

### 배포 검색

```python
deliveries = client.search_deliveries(
    status='completed',  # scheduled, sent, completed, failed
    limit=10,
    offset=0,
    date_from='2024-01-01',
    date_to='2024-12-31'
)

for d in deliveries['deliveries']:
    print(f"{d['deliveryId']}: {d['status']}")
```

### 주소록에 수신자 추가

```python
client.add_recipient_to_address_book(
    address_book_id='book-123',
    phone_number='+819012345678',
    name='John Doe',
    attributes={'customer_id': '12345', 'plan': 'premium'}
)
```

### 배포 수신자 목록 조회

```python
recipients = client.get_delivery_recipients(
    delivery_id='delivery-123',
    limit=20
)

for r in recipients['recipients']:
    print(f"{r['phoneNumber']}: {r['status']}")
    if r['status'] == 'failed':
        print(f"  Error: {r['errorMessage']}")
```

## 주요 기능

1. **주소록 관리**: 생성, 조회, 업데이트, 삭제
2. **SMS 배포**: 전화번호 또는 주소록으로 배포
3. **예약 배포**: 지정된 시간에 배포
4. **배포 추적**: 송신, 전달, 실패 상태 확인
5. **수신자 관리**: 주소록에 연락처 추가

## 전화번호 형식

국제 전화번호 형식 사용:
- `+81` (일본 국가 코드)
- 11자리 (총)
- 예: `+819012345678`

## 일본어 메시지

UTF-8 인코딩 지원:
- 한자, 히라가나, 카타카나 모두 전송 가능
- 반각/전각 글자 모두 지원

## 배포 상태

- `scheduled`: 예약됨 (송신 대기)
- `sent`: 송신됨
- `completed`: 완료 (모든 메시지 전달)
- `failed`: 실패

## 에러 처리

```python
from cuenote_sms_client import CuenoteSMSError, RateLimitError

try:
    delivery = client.create_sms_delivery_phone_numbers(
        phone_numbers=['+819012345678'],
        message='Test message'
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except CuenoteSMSError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 10 요청
- 무료 요금제: 월 500 메시지
- 유료 요금제: 무제한 메시지

## 예약 시간 형식

ISO 8601 형식 사용:
- `2024-02-28T10:00:00Z` (UTC)
- `2024-02-28T19:00:00+09:00` (일본 시간)

## URL 추적

`track_urls=True`로 설정하면 메시지 내 URL의 클릭을 추적할 수 있습니다.

## 지원

자세한 API 문서: [Cuenote API Documentation](https://www.cuenote.jp/api/)