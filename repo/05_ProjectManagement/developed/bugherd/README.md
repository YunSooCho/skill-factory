#BugHerd APIクライアント

BugHerd用のPython APIクライアントです。バグ追跡機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

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

##ライセンス

MIT License