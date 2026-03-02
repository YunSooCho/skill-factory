#Bizer Team APIクライアント

Bizer Team用のPython APIクライアント。チーム管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from bizer_team import BizerTeamClient, BizerTeamError

client = BizerTeamClient(api_key="YOUR_API_KEY")

# 팀 조회
teams = client.get_teams()

# 작업 생성
task = client.create_task("team_id", {"name": "Task", "description": "Description"})
```

##ライセンス

MIT License