# Crowdin API 클라이언트

Crowdin을 위한 Python API 클라이언트입니다. 현지화 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from crowdin import CrowdinClient, CrowdinError

client = CrowdinClient(access_token="YOUR_ACCESS_TOKEN")

# 프로젝트 조회
projects = client.list_projects()

# 번역 상태 조회
status = client.get_translation_status("project_id")
```

## 라이선스

MIT License