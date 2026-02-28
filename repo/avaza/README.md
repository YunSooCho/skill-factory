# Avaza API 클라이언트

Avaza를 위한 Python API 클라이언트입니다. 비즈니스 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from avaza import AvazaClient, AvazaError

client = AvazaClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({
    "ProjectId": "project_id",
    "Name": "Task Name"
})
```

## 라이선스

MIT License