# Vapi API 클라이언트

Vapi를 위한 Python API 클라이언트입니다. 음성 통화 자동화 기능을 제공합니다.

## 개요

Vapi는 AI 기반 음성 통화 자동화 서비스입니다. 통화 생성, 로그 검색, 분석 등의 기능을 제공합니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Vapi](https://vapi.ai/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from vapi import VapiClient, VapiError

client = VapiClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 발신 통화 생성

```python
result = client.create_outbound_call(
    phone_number="+821012345678",
    assistant_id="assistant_id_here",
    customer_name="John Doe"
)

call_id = result.get("id")
print(f"Call ID: {call_id}")
```

### 통화 검색

```python
result = client.search_calls(
    limit=10,
    status="completed",
    assistant_id="assistant_id_here"
)

for call in result.get("calls", []):
    print(f"- {call.get('id')}: {call.get('status')}")
```

### 로그 검색

```python
result = client.search_logs(
    call_id="call_id_here",
    level="info",
    limit=50
)
```

### 데이터 분석

```python
result = client.search_data_analytics(
    start_date="2024-01-01",
    end_date="2024-01-31",
    metrics=["call_count", "duration", "success_rate"],
    group_by="day"
)
```

### 파일 업로드

```python
result = client.upload_file(
    file="audio.mp3",
    file_type="audio",
    name="greeting"
)

file_id = result.get("id")
print(f"File ID: {file_id}")
```

### 통화 상세 조회

```python
call = client.get_call("call_id_here")
print(f"Status: {call.get('status')}")
print(f"Duration: {call.get('duration')}")
```

## 에러 처리

```python
try:
    result = client.create_outbound_call(phone_number, assistant_id)
except VapiAuthenticationError:
    print("API 키가 올바르지 않습니다")
except VapiRateLimitError:
    print("속도 제한이 초과되었습니다")
except VapiError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License

## 지원

- [Vapi 공식 사이트](https://vapi.ai/)
- [Vapi 문서](https://docs.vapi.ai/)