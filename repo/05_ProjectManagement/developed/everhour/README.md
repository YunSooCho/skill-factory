# Everhour API 클라이언트

Everhour를 위한 Python API 클라이언트입니다. 시간 추적 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from everhour import EverhourClient, EverhourError

client = EverhourClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 시간 기록 생성
entry = client.create_time_entry({"task": "123", "hours": 2.5})
```

## 라이선스

MIT License