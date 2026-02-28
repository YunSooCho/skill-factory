# Float API 클라이언트

Float를 위한 Python API 클라이언트입니다. 인력 스케줄링 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from float import FloatClient, FloatError

client = FloatClient(api_token="YOUR_API_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 스케줄 조회
schedules = client.get_schedules("2024-01-01", "2024-01-31")
```

## 라이선스

MIT License