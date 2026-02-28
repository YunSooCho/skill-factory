# Awork API 클라이언트

Awork를 위한 Python API 클라이언트입니다. 작업 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from awork import AworkClient, AworkError

client = AworkClient(api_token="YOUR_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"projectId": "123", "name": "Task"})
```

## 라이선스

MIT License