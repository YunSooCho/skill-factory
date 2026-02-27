# Bitly API Integration

Bitly의 REST API를 사용하여 링크 단축 및 클릭 추적을 수행하는 Python 라이브러리입니다.

## 설치

```bash
pip install requests
```

## 사용법

### 클라이언트 초기화

```python
from bitly import BitlyClient

client = BitlyClient(access_token="your_access_token_here")
```

### 링크 단축

```python
# 간단한 링크 단축
result = client.shorten_link(
    long_url="https://example.com/very/long/url"
)
print(result["link"])  # https://bit.ly/2XxYyZz

# 커스텀 도메인과 태그
result = client.create_bitlink(
    long_url="https://example.com/product",
    domain="bit.ly",
    title="Product Page",
    tags=["product", "marketing"],
    notes="Product launch link"
)
```

### 링크 확장

```python
# 원본 URL 확인
expanded = client.expand_bitlink(
    bitlink="https://bit.ly/2XxYyZz"
)
print(expanded["long_url"])
```

### 링크 검색

```python
# Bitlink 검색
results = client.search_bitlinks(
    group_guid="your_group_guid",
    tags=["marketing"],
    limit=20
)

# 도메인별 검색
results = client.search_bitlinks(
    domain="bit.ly",
    created_after="2024-01-01T00:00:00Z"
)
```

### 링크 삭제

```python
# Bitlink 삭제
client.delete_bitlink(bitlink="https://bit.ly/2XxYyZz")
```

### 클릭 추적

```python
# 클릭 수
clicks = client.get_clicks(
    bitlink="https://bit.ly/2XxYyZz",
    unit="day",
    units=-1
)
print(clicks["total_clicks"])

# 클릭 요약
summary = client.get_click_summary(
    bitlink="https://bit.ly/2XxYyZz",
    unit="week",
    units=4
)

# 국가별 클릭
by_country = client.get_clicks_by_country(
    bitlink="https://bit.ly/2XxYyZz",
    unit="month",
    units=12
)
```

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/shorten` | POST | 링크 단축 |
| `/bitlinks` | POST | Bitlink 생성 (확장) |
| `/expand` | POST | 링크 확장 |
| `/bitlinks/{id}` | DELETE | 링크 삭제 |
| `/bitlinks/{id}/clicks` | GET | 클릭 데이터 |
| `/bitlinks/{id}/clicks/summary` | GET | 클릭 요약 |
| `/bitlinks/{id}/clicks/countries` | GET | 국가별 클릭 |

## 예외 처리

```python
from bitly import BitlyClient, BitlyAPIError, BitlyAuthError

try:
    result = client.shorten_link(long_url="https://example.com")
except BitlyAuthError as e:
    print("인증 오류:", e)
except BitlyAPIError as e:
    print("API 오류:", e)
```

## API 메서드

| 메서드 | 설명 |
|--------|------|
| `shorten_link()` | 간단한 링크 단축 |
| `create_bitlink()` | 확장 옵션으로 링크 생성 |
| `expand_bitlink()` | 링크 확장 |
| `search_bitlinks()` | Bitlink 검색 |
| `delete_bitlink()` | 링크 삭제 |
| `get_clicks()` | 클릭 수 조회 |
| `get_click_summary()` | 클릭 요약 조회 |
| `get_clicks_by_country()` | 국가별 클릭 조회 |

## 인증

Bitly API는 Access Token을 사용합니다. 다음에서 생성 가능합니다:
- [Bitly Developer Portal](https://dev.bitly.com/authentication.html)

## API 참조

- [Bitly API Reference](https://dev.bitly.com/api-reference/)