# ClickUp API 클라이언트

ClickUp을 위한 Python API 클라이언트입니다. 프로젝트 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from clickup import ClickUpClient, ClickUpError

client = ClickUpClient(api_token="YOUR_API_TOKEN")

# 작업 조회
tasks = client.get_tasks("list_id")

# 작업 생성
task = client.create_task("list_id", {
    "name": "Task name",
    "description": "Description"
})
```

## 라이선스

MIT License