# Wachete API 클라이언트

Wachete를 위한 Python API 클라이언트입니다. 웹페이지 모니터링 기능을 제공합니다.

## 개요

Wachete는 웹페이지 변경을 모니터링하는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Wachete](https://wachete.com/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from wachete import WacheteClient, WacheteError

client = WacheteClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### Wachet 생성

```python
result = client.create_wachet(
    url="https://example.com",
    name="Monitor Homepage",
    check_interval=3600,
    email_notification=True
)
```

### Wachet 조회

```python
wachet = client.get_wachet("wachet_id_here")
```

### Wachet 검색

```python
result = client.search_wachets(
    limit=20,
    status="active"
)

for wachet in result.get("wachets", []):
    print(f"- {wachet.get('name')}")
```

### Wachet 업데이트

```python
result = client.update_wachet(
    wachet_id="wachet_id_here",
    check_interval=1800,
    name="Updated Name"
)
```

### Wachet 삭제

```python
result = client.delete_wachet("wachet_id_here")
```

### 변경 이력 조회

```python
result = client.get_wachet_changes("wachet_id_here", limit=10)
```

## 에러 처리

```python
try:
    result = client.create_wachet(url, name)
except WacheteAuthenticationError:
    print("API 키가 올바르지 않습니다")
except WacheteRateLimitError:
    print("속도 제한이 초과되었습니다")
except WacheteError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Wachete 공식 사이트](https://wachete.com/)
- [Wachete 문서](https://docs.wachete.com/)