#ClickUp APIクライアント

ClickUp用のPython APIクライアントです。プロジェクト管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from clickup import ClickUpClient, ClickUpError

client = ClickUpClient(api_token="YOUR_API_TOKEN")

# 작업 조회
tasks = client.get_tasks("list_id")

# 작업 생성
task = client.create_task("list_id", {
    "name": "Task name",
    "description": "Description"
})
```

##ライセンス

MIT License