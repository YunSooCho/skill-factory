#Avaza APIクライアント

Avaza用のPython APIクライアントです。ビジネス管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

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

##ライセンス

MIT License