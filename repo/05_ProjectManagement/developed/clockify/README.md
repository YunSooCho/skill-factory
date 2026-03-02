#Clockify APIクライアント

Clockify用のPython APIクライアント。時間追跡機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from clockify import ClockifyClient, ClockifyError

client = ClockifyClient(api_key="YOUR_API_KEY", workspace_id="WORKSPACE_ID")

# 프로젝트 조회
projects = client.get_projects()

# 시간 기록 생성
entry = client.create_time_entry({
    "description": "Task description",
    "projectId": "project_id"
})
```

##ライセンス

MIT License