# Mailersend API 클라이언트

Mailersend를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Mailersend API에 접근하여 각종 CRUD 작업 및 이벤트 처리를 지원합니다.

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

1. Mailersend 개발자 포털에서 앱 생성
2. API 키/토큰 발급
3. 발급된 API 키/토큰 저장

## 사용법

### 초기화

```python
from mailersend import Client

client = Client(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 예시 코드

```python
# CRUD 작업
try:
    result = client.list_items()
    print("Items:", result)
except Exception as e:
    print("Error:", str(e))
```

## API 액션

- `from_dict` - API method
- `close` - Close the session.

## 에러 처리

```python
try:
    result = client.your_method()
except Exception as e:
    print("Error:", str(e))
```

## Rate Limiting

API 요청 간 최소 0.1초 지연이 적용됩니다.

## 라이선스

MIT License