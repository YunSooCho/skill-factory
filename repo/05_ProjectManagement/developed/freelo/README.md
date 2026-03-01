# Freelo API 클라이언트

Freelo를 위한 Python API 클라이언트입니다. 작업 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from freelo import FreeloClient, FreeloError

client = FreeloClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"name": "Task", "description": "Description"})

# 코멘트 추가
comment = client.create_comment("task_id", {"text": "Comment text"})
```

## 라이선스

MIT License