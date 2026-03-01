# Zoho Writer API 클라이언트

Zoho Writer를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Zoho Writer API에 접근하여 각종 CRUD 작업 및 이벤트 처리를 지원합니다.

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

1. Zoho Writer 개발자 포털에서 앱 생성
2. API 키/토큰 발급
3. 발급된 API 키/토큰 저장

## 사용법

### 초기화

```python
from zoho_writer.client import ZohoWriterClient

client = ZohoWriterClient(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 예시 코드

```python
# CRUD 작업
try:
    result = client.create_item({"name": "test"})
    print("Created:", result)
except Exception as e:
    print("Error:", str(e))

# 리스트 조회
items = client.list_items()
for item in items:
    print(item['id'], item['name'])
```

## API 액션

- `_wait_for_rate_limit` - Apply rate limiting to requests
- `_update_rate_limit` - Update rate limit information from response headers
- `close` - Close the session
- `__enter__` - Context manager entry
- `__exit__` - Context manager exit

## Webhook 트리거

- **Webhook** - 이 서비스는 Webhook 트리거를 지원합니다

## 에러 처리

```python
try:
    result = client.your_method()
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청 간 최소 0.1초 지연이 적용됩니다. 너무 많은 요청이 발생하면 Rate Limit 에러가 발생할 수 있습니다.

## 라이선스

MIT License