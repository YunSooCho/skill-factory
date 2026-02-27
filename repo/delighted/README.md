# Delighted API Client

Delighted용 Python 클라이언트 - 고객 만족도 설문 및 피드백 관리

## 설치

```bash
pip install -r requirements.txt
```

## API Key 획득

1. [Delighted 계정 생성](https://delighted.com/)
2. 로그인 후 Settings > API Keys 접근
3. 각 Project별 API 키 생성
5. API 키 복사

## 사용법

### 클라이언트 초기화

```python
from delighted_client import create_delighted_client

client = create_delighted_client(api_key='your-api-key')
```

### NPS 메트릭 조회

```python
metrics = client.get_metrics(
    since='2024-01-01',  # 선택: 시작 날짜
    until='2024-12-31',  # 선택: 종료 날짜
    trend='30d'  # 선택: 트렌드 기간
)

print(f"NPS Score: {metrics['nps']}")
print(f"Total Responses: {metrics['total_responses']}")
```

### 사람 생성

```python
person = client.create_person(
    email='customer@example.com',
    name='John Doe',
    properties={'plan': 'premium', 'signup_date': '2024-01-15'},
    locale='en',  # 언어 설정
    send=True  # 즉시 설문조사 전송
)

print(f"Created person with ID: {person.get('id')}")
```

### 사람 업데이트

```python
client.update_person(
    person_id='person-123',
    updates={
        'name': 'Jane Doe',
        'properties': {'plan': 'enterprise'}
    }
)
```

### 사람 검색

```python
# 이메일로 검색
people = client.search_people(email='customer@example.com')
for person in people:
    print(f"{person['email']}: {person['name']}")
```

### 설문응답 검색

```python
responses = client.search_survey_responses(
    per_page=20,
    since='2024-01-01',
    min_score=7,  # 점수 7 이상만
    max_score=10
)

for response in responses:
    print(f"Score: {response['score']}, Comment: {response.get('comment', 'N/A')}")
```

### 사람 구독 취소

```python
client.unsubscribe_people(email='customer@example.com')
# 또는
client.unsubscribe_people(person_id='person-123')
```

### 응답 추가 (외부 소스에서)

```python
client.add_survey_response(
    person_email='customer@example.com',
    score=9,
    comment='Great service!',
    properties={'source': 'phone'}
)
```

## 웹훅 핸들러

Delighted에서 새 응답이나 구독 취소 이벤트를 수신하려면 웹훅 서버를 실행하세요:

```python
from delighted_client import DelightedWebhookHandler

# 핸들러 초기화
webhook = DelightedWebhookHandler(port=5000)

# 이벤트 핸들러 등록
@webhook.on_new_response
def handle_response(data):
    print(f"New response: {data}")

@webhook.on_new_unsubscribe
def handle_unsubscribe(data):
    print(f"Unsubscribe: {data}")

# 서버 시작
webhook.run(host='0.0.0.0')

# 또는 백그라운드에서 실행하려면:
import time
thread = webhook.run(host='0.0.0.0', debug=False)
# 메인 스레드 유지
while True:
    time.sleep(1)
```

Delighted 대시보드에서 웹훅 URL을 설정하세요:
`https://your-server.com/webhook`

## 주요 기능

1. **NPS 메트릭**: 넷 프로모터 스코어 계산
2. **사람 관리**: 생성, 업데이트, 검색
3. **설문 응답**: 응답 조회 및 필터링
4. **구독 관리**: 구독 취소 처리
5. **웹훅**: 실시간 이벤트 수신

## 에러 처리

```python
from delighted_client import DelightedError, RateLimitError

try:
    metrics = client.get_metrics()
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after: {e}")
except DelightedError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 10 요청
- Rate limit 초과 시 429 응답
- 무료 요금제: 월 250 설문응답

## 지원

자세한 API 문서: [Delighted API Documentation](https://delighted.com/docs/api)