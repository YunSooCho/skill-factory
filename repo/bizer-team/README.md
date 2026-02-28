# Bizer Team API 클라이언트

Bizer Team를 위한 Python API 클라이언트입니다. 팀 관리 기능을 제공합니다.

## 설치

```bash
pip install requests
```

## 사용법

```python
from bizer_team import BizerTeamClient, BizerTeamError

client = BizerTeamClient(api_key="YOUR_API_KEY")

# 팀 조회
teams = client.get_teams()

# 작업 생성
task = client.create_task("team_id", {"name": "Task", "description": "Description"})
```

## 라이선스

MIT License