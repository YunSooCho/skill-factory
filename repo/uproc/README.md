# Uproc API 클라이언트

Uproc를 위한 Python API 클라이언트입니다. 데이터 처리 기능을 제공합니다.

## 개요

Uproc는 데이터 행 처리 및 배치 처리 기능을 제공하는 서비스입니다.

## 설치

```bash
pip install requests
```

또는:

```bash
pip install -r requirements.txt
```

## API 키 발급

1. [Uproc](https://uproc.com/)에서 계정 생성
2. API 키 발급
3. API 키를 안전하게 저장

## 사용법

### 초기화

```python
from uproc import UprocClient, UprocError

client = UprocClient(
    api_key="YOUR_API_KEY",
    timeout=60
)
```

### 단일 행 처리

```python
result = client.process_row(
    row_data={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-555-1234"
    },
    process_type="standard"
)
```

### 여러 행 처리

```python
rows = [
    {"name": "John", "score": 85},
    {"name": "Jane", "score": 92},
    {"name": "Bob", "score": 78}
]

result = client.process_multiple_rows(
    rows=rows,
    process_type="batch"
)
```

### 작업 상태 확인

```python
status = client.get_job_status("job_id_here")
print(f"Status: {status.get('status')}")
```

## 에러 처리

```python
try:
    result = client.process_row(row_data)
except UprocAuthenticationError:
    print("API 키가 올바르지 않습니다")
except UprocRateLimitError:
    print("속도 제한이 초과되었습니다")
except UprocError as e:
    print(f"요청 실패: {str(e)}")
```

## 라이선스

MIT License