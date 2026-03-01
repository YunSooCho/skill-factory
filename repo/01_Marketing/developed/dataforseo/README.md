# DataForSEO API Client

DataForSEO용 Python 클라이언트 - SEO 데이터 및 분석

## 설치

```bash
pip install -r requirements.txt
```

## API Credentials 획득

1. [DataForSEO 계정 생성](https://dataforseo.com/)
2. Dashboard에서 API Login과 API Password 획득
3. Settings > API API Credentials 접근
4. Login과 Password 복사

## 사용법

### 클라이언트 초기화

```python
from dataforseo_client import create_dataforseo_client

client = create_dataforseo_client(
    api_login='your-api-login',
    api_password='your-api-password'
)
```

### 검색량 및 경쟁 데이터 조회

```python
result = client.get_search_volume(
    keywords=['python programming', 'machine learning', 'data science'],
    location_code=2840,  # Global (default)
    language_code='en'
)

for item in result['tasks'][0]['result']:
    kw = item['keyword']
    volume = item['search_volume']
    cpc = item['cpc']
    competition = item['competition']

    print(f"{kw}: Volume={volume}, CPC=${cpc:.2f}, Competition={competition:.2f}")
```

### SERP 데이터 조회

```python
serp = client.get_serp_data(
    keyword='python tutorial',
    location_code=2840,
    language_code='en',
    search_engine='google',
    depth=10
)

for result in serp['tasks'][0]['result'][0]['items']:
    print(f"{result['title']}: {result.get('url', 'N/A')}")
```

### 도메인 랭크 개요

```python
rank = client.get_domain_rank_overview(
    target='example.com',
    language_code='en'
)

domain_auth = rank['tasks'][0]['result'][0]['domain_authority']
page_auth = rank['tasks'][0]['result'][0]['page_authority']

print(f"DA: {domain_auth}, PA: {page_auth}")
```

### 백링크 데이터 조회

```python
backlinks = client.get_backlink_data(
    target='example.com',
    limit=100,
    filters=[
        ["dofollow", "=", True],  # Dofollow 링크만
        ["type", "in", ["link", "redirect"]]
    ]
)

for bl in backlinks['tasks'][0]['result'][0]['backlinks']:
    print(f"{bl['domain_from']} -> PA={bl['page_authority']}")
```

### 백링크 요약

```python
summary = client.get_backlink_summary(target='example.com')

total = summary['tasks'][0]['result'][0]['total']
dofollow = summary['tasks'][0]['result'][0]['dofollow']

print(f"Total: {total}, Dofollow: {dofollow}")
```

### 비즈니스 목록 검색 (Google Maps, etc.)

```python
businesses = client.search_business_listings(
    query='restaurants',
    location_name='New York',
    depth=10
)

for item in businesses['tasks'][0]['result'][0]['items']:
    print(f"{item['title']}")
    print(f"  Rating: {item.get('rating', 'N/A')}")
    print(f"  Phone: {item.get('phone', 'N/A')}")
    print(f"  Address: {item.get('address', 'N/A')}")
```

## 위치 및 언어 코드

DataForSEO는 표준 위치 및 언어 코드를 사용합니다:

- **Location Code**: [DataForSEO Location Codes](https://docs.dataforseo.com/v3/serp/google/locations/)
  - 2840: Global
  - 2840: USA
  - 2840: UK
  - 2840: Japan

- **Language Code**: ISO 639-1 (en, ja, ko, de, fr, etc.)

## 주요 기능

1. **검색량 데이터**: 키워드 검색량, CPC, 경쟁도
2. **SERP 데이터**: 검색 결과 페이지 분석
3. **도메인 랭크**: DA, PA 및 백링크 정보
4. **백링크 분석**: 백링크 요약 및 세부 정보
5. **비즈니스 목록**: Google Maps 비즈니스 데이터

## 에러 처리

```python
from dataforseo_client import DataForSEOError, RateLimitError

try:
    result = client.get_search_volume(['python'])
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except DataForSEOError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 50 요청
- 무료 평가판: 데이터 조회 무료
- 유료 요금제: 종량제 (API 사용량 기반)

## 비동기 작업

일부 작업은 비동기로 처리됩니다. 작업 ID를 사용하여 결과를 조회:

```python
# 작업 제출
task_id = "your-task-id"

# 결과 조회
result = client.get_task_result(task_id)
```

## 지원

자세한 API 문서: [DataForSEO API Documentation](https://docs.dataforseo.com/v3/)