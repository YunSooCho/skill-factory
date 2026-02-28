# Mailparser.io API 클라이언트

Mailparser.io를 위한 Python API 클라이언트입니다.

## 개요

이 클라이언트는 Mailparser.io API에 접근하여 이메일 파싱 및 데이터 추출 작업을 지원합니다.

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

1. [Mailparser.io](https://www.mailparser.io/)에서 계정 생성
2. API 키 발급
3. 발급된 API 키 저장

## 사용법

### 초기화

```python
from mailparser_io import Client

client = Client(
    api_key="YOUR_API_KEY",
    timeout=30
)
```

### 예시 코드

```python
# 이메일 파싱
try:
    result = client.parse_email(email_data)
    print("Parsed email:", result)
except Exception as e:
    print("Error:", str(e))
```

## API 액션

- `list_items` - 항목 리스트 조회
- `get_item` - 항목 상세 조회
- `create_item` - 새 항목 생성

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