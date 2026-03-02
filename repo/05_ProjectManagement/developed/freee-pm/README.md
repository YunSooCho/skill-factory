#Freee PM API クライアント

Freee PM用のPython APIクライアント。プロジェクト管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from freee_pm import FreeePMClient, FreeePMError

client = FreeePMClient(access_token="YOUR_ACCESS_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"name": "Task", "project_id": "123"})
```

##ライセンス

MIT License