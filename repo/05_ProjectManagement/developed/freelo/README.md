#Freelo API クライアント

Freelo用のPython APIクライアントです。ジョブ管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from freelo import FreeloClient, FreeloError

client = FreeloClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"name": "Task", "description": "Description"})

# 코멘트 추가
comment = client.create_comment("task_id", {"text": "Comment text"})
```

##ライセンス

MIT License