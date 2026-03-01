# BugHerd API 클라이언트

BugHerd를 위한 Python API 클라이언트입니다. 버그 추적 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from bugherd import BugHerdClient, BugHerdError

client = BugHerdClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 버그 생성
task = client.create_task("project_id", {
    "description": "Bug description",
    "priority": "high"
})
```

## 라이선스

MIT License