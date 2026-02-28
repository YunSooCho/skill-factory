# Frictio API 클라이언트

Frictio를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Frictio API에 접근하여 각종 CRUD 작업 및 이벤트 처리를 지원합니다.

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

1. Frictio 개발자 포털에서 앱 생성
2. API 키/토큰 발급
3. 발급된 API 키/토큰 저장

## 사용법

### 초기화

```python
from frictio.client import FrictioClient

client = FrictioClient(
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

- `__init__` - Initialize Frictio webhook client Args: webhook_secret: Secret key for webhook s...
- `register_event_handler` - Register a handler for a specific event type Args: event_type: Event type to han...
- `unregister_event_handler` - Unregister an event handler
- `on_meeting_ended` - Register handler for meeting ended events Event data structure example: { "event...
- `on_playbook_result_updated` - Register handler for playbook result updated events Event data structure example...
- `on_playbook_generated` - Register handler for playbook generated events Event data structure example: { "...

## Webhook 트리거

- **Register Event Handler** - Register a handler for a specific event type Args: event_typ...
- **Unregister Event Handler** - Unregister an event handler

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