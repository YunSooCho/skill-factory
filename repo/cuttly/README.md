# Cuttly API Client

Cuenote SMS용 Python 클라이언트 - URL 단축 및 분석 API

## 설치

```bash
pip install -r requirements.txt
```

## API Key 획득

1. [Cuttly 계정 생성](https://cutt.ly/)
2. 로그인 후 Dashboard 접근
3. Settings > API Keys 메뉴에서 API 키 생성
4. API 키 복사

## 사용법

### 기본 클라이언트 초기화

```python
from cuttly_client import create_cuttly_client

# API 키로 클라이언트 생성
client = create_cuttly_client(api_key='your-api-key')
```

### URL 단축

```python
result = client.shorten_url(
    url='https://example.com/very-long-url',
    name='my-custom-link',  # 선택: 사용자 정의 이름
    tags=['marketing', 'social'],  # 선택: 태그
    public=False  # 선택: 공개 여부
)

short_link = result['url']['shortLink']
print(f"Short URL: {short_link}")
```

### 분석 데이터 조회

```python
analytics = client.get_analytics(
    url='https://cutt.ly/my-custom-link',
    limit=100,  # 선택: 최대 결과 수
    date_from='2024-01-01',  # 선택: 시작 날짜
    date_to='2024-12-31'  # 선택: 종료 날짜
)

print(f"Total clicks: {analytics['url']['clicks']}")
```

## 주요 기능

1. **URL 단축**: 긴 URL을 짧은 링크로 변환
2. **분석 데이터**: 클릭 수, 리퍼러, 위치 등 조회
3. **사용자 정의 이름**: 원하는 짧은 URL 지정 가능
4. **태그 지원**: 링크를 태그로 분류

## 에러 처리

```python
from cuttly_client import CuttlyError, RateLimitError

try:
    result = client.shorten_url('https://example.com')
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except CuttlyError as e:
    print(f"API error: {e}")
```

## API 제한

- 기본 제한: 초당 10 요청
- 무료 요금제: 월 1,000 단축
- Rate limit 초과 시 429 에러 반환

## 지원

자세한 API 문서: [Cuttly API Documentation](https://cutt.ly/api-documentation)