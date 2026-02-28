# Backlog API 클라이언트

Backlog를 위한 Python API 클라이언트입니다. 프로젝트 및 이슈 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from backlog import BacklogClient, BacklogError

client = BacklogClient(space_key="your-space", api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 이슈 생성
issue = client.create_issue({
    "projectId": "123",
    "summary": "New task",
    "description": "Description"
})
```

## 라이선스

MIT License