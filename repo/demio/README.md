# Demio API Client

Demio용 Python 클라이언트 - 웨비나 플랫폼 자동화

## 설치

```bash
pip install -r requirements.txt
```

## API Credentials 획득

1. [Demio 계정 생성](https://demio.com/)
2. 로그인 후 Settings > Integrations > API 접근
3. API Key와 API Secret 생성
4. 자격 증명 복사

## 사용법

### 클라이언트 초기화

```python
from demio_client import DemioClient

client = DemioClient(
    api_key='your-api-key',
    api_secret='your-api-secret'
)
```

### 이벤트 목록 조회

```python
events = client.list_events(
    status='scheduled',  # scheduled, completed, active, cancelled
    limit=10
)

for event in events['events']:
    print(f"{event['name']}: {event['start_date']}")
```

### 이벤트 상세 조회

```python
event = client.get_event(event_id=12345)
print(f"Event: {event['name']}")
print(f"Status: {event['status']}")
print(f"Duration: {event['duration']} minutes")
```

### 이벤트 참여자 목록

```python
participants = client.list_event_participants(
    event_id=12345,
    limit=20
)

for p in participants['participants']:
    print(f"{p['name']} ({p['email']}): Attended {p['is_attended']}")
```

### 이벤트 등록자 목록

```python
registrants = client.get_event_registrants(event_id=12345)

for r in registrants['registrants']:
    print(f"{r['email']}: {r['join_link']}")
```

### 참여자 등록

```python
result = client.register_event_participant(
    event_id=12345,
    email='new@example.com',
    name='New Participant',
    first_name='New',
    last_name='Participant',
    custom_fields={'company': 'Acme Corp'}
)

print(f"Join link: {result['join_link']}")
print(f"UUID: {result['uuid']}")
```

### 등록 취소

```python
client.cancel_registration(
    event_id=12345,
    email='new@example.com'
)
```

### 다가오는 이벤트 조회

```python
upcoming = client.get_upcoming_events(limit=5)
```

### 완료된 이벤트 조회

```python
completed = client.get_completed_events(limit=10)
```

## 주요 기능

1. **이벤트 관리**: 웨비나 이벤트 조회
2. **참여자 관리**: 등록, 참여 조회
3. **자동화**: 웨비나 등록 자동화
4. **분석**: 참여자 데이터 추출

## 에러 처리

```python
from demio_client import DemioError, RateLimitError

try:
    event = client.get_event(12345)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DemioError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 10 요청
- 무료 요금제: 월 50 참여자
- 유료 요금제: 무제한

## 지원

자세한 API 문서: [Demio API Documentation](https://demio.com/docs/developers/)