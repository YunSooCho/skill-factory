#Awork APIクライアント

Awork用のPython APIクライアントです。ジョブ管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from awork import AworkClient, AworkError

client = AworkClient(api_token="YOUR_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 작업 생성
task = client.create_task({"projectId": "123", "name": "Task"})
```

##ライセンス

MIT License