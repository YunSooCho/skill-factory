# Scraptio API 클라이언트

Scraptio를 위한 Python API 클라이언트입니다. 웹사이트에서 텍스트, 링크, 이메일을 쉽게 추출할 수 있습니다.

## 개요

Scraptio는 복잡한 웹 스크래핑을 단순화한 서비스입니다. Zapier, Make 및 기타 자동화 도구와 연동하여 웹사이트 데이터를 자동으로 추출할 수 있습니다.

## 설치

의존성 패키지:

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Scraptio](https://scraptio.com/)에서 계정 생성
2. 무료 플랜으로 시작 (월 30회 요청)
3. 대시보드에서 API 키 확인 또는 발급
4. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from scraptio import ScraptioClient, ScraptioError

client = ScraptioClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 기본 URL 스크래핑

```python
try:
    result = client.scrape_url("https://example.com")
    print("Scraped data:", result)
except ScraptioError as e:
    print("Error:", str(e))
```

### CSS 선택자로 특정 데이터 추출

```python
css_selectors = {
    "title": "h1",
    "description": ".description",
    "price": ".price"
}

result = client.scrape_url(
    "https://example.com",
    css_selectors=css_selectors
)
```

### 이메일 추출

```python
result = client.scrape_url(
    "https://example.com/contact",
    extract_emails=True
)
print("Emails:", result.get("emails", []))
```

### 링크 추출

```python
result = client.scrape_url(
    "https://example.com",
    extract_links=True
)
print("Links:", result.get("links", []))
```

### 대기 시간 설정 (자바스크립트 렌더링 대기)

```python
result = client.scrape_url(
    "https://example.com",
    wait=2000  # 2초 대기
)
```

### 스크래핑 결과 조회

```python
# 비동기 스크래핑인 경우 결과 ID로 조회
result = client.get_scrape_result("scrape_id_here")
```

### 최근 스크래핑 목록

```python
result = client.list_scrapes(limit=20, offset=0)
print("Recent scrapes:", result.get("scrapes", []))
```

## API 메서드

### scrape_url

웹사이트 URL을 스크래핑하여 데이터를 추출합니다.

**매개변수:**
- `url` (str): 스크래핑할 URL (필수)
- `wait` (int, optional): 스크래핑 전 대기 시간 (밀리초)
- `css_selectors` (dict, optional): 필드 이름과 CSS 선택자 매핑
- `extract_emails` (bool): 이메일 추출 여부 (기본값: False)
- `extract_links` (bool): 링크 추출 여부 (기본값: False)
- `extract_texts` (bool): 텍스트 추출 여부 (기본값: True)

**반환값:**
- `dict`: 추출된 데이터를 포함한 딕셔너리

### get_scrape_result

비동기 스크래핑 작업의 결과를 조회합니다.

**매개변수:**
- `scrape_id` (str): 스크래핑 작업 ID

**반환값:**
- `dict`: 스크래핑 결과

### list_scrapes

최근 스크래핑 작업 목록을 조회합니다.

**매개변수:**
- `limit` (int): 반환할 결과 수 (기본값: 10)
- `offset` (int): 건너뛸 결과 수 (기본값: 0)

**반환값:**
- `dict`: 스크래핑 작업 목록

## 에러 처리

```python
from scraptio import ScraptioError, ScraptioRateLimitError, ScraptioAuthenticationError

try:
    result = client.scrape_url("https://example.com")
except ScraptioAuthenticationError:
    print("API 키가 올바르지 않습니다")
except ScraptioRateLimitError:
    print("속도 제한이 초과되었습니다. 잠시 후 다시 시도하세요")
except ScraptioError as e:
    print(f"스크래핑 실패: {str(e)}")
```

## Rate Limiting

API 요청 간 최소 100ms 지연이 자동으로 적용됩니다.

## 예시 코드

### 전체 예시

```python
from scraptio import ScraptioClient, ScraptioError

# 클라이언트 초기화
client = ScraptioClient(api_key="YOUR_API_KEY")

# 웹사이트 스크래핑
try:
    # 텍스트, 링크, 이메일 추출
    result = client.scrape_url(
        "https://example.com",
        extract_emails=True,
        extract_links=True
    )

    print("Title:", result.get("title"))
    print("Text:", result.get("text", "")[:200])  # 첫 200자
    print("Links found:", len(result.get("links", [])))
    print("Emails found:", len(result.get("emails", [])))

    # 최근 스크래핑 내역 확인
    history = client.list_scrapes(limit=5)
    print(f"Total scrapes: {history.get('total', 0)}")

except ScraptioError as e:
    print(f"Error: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Scraptio 공식 사이트](https://scraptio.com/)
- [Scraptio 문서](https://scraptio.notion.site/)
- [Zapier 통합 가이드](https://scraptio.notion.site/How-to-use-Scraptio-with-Zapier-45ba2b93ffb94df5966d0a9f9b7394a2)
- [Make 통합 가이드](https://scraptio.notion.site/How-to-use-Scraptio-with-Make-2a727a5acb8746bf9eed039661781722)