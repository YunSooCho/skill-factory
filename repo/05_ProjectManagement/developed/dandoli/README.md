# Dandoli API 클라이언트

Dandoli를 위한 Python API 클라이언트입니다. 작업 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from dandoli import DandoliClient, DandoliError

client = DandoliClient(api_key="YOUR_API_KEY")

# 작업 조회
tasks = client.get_tasks()

# 작업 생성
task = client.create_task({"title": "Task", "description": "Description"})
```

## 라이선스

MIT License