#Dandoli APIクライアント

Dandoli用のPython APIクライアントです。ジョブ管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from dandoli import DandoliClient, DandoliError

client = DandoliClient(api_key="YOUR_API_KEY")

# 작업 조회
tasks = client.get_tasks()

# 작업 생성
task = client.create_task({"title": "Task", "description": "Description"})
```

##ライセンス

MIT License