# Freee PM API 클라이언트

Freee PM을 위한 Python API 클라이언트입니다. 프로젝트 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from freee_pm import FreeePMClient, FreeePMError

client = FreeePMClient(access_token="YOUR_ACCESS_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"name": "Task", "project_id": "123"})
```

## 라이선스

MIT License