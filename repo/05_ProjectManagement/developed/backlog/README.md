#Backlog APIクライアント

Backlog用のPython APIクライアント。プロジェクトと課題管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from backlog import BacklogClient, BacklogError

client = BacklogClient(space_key="your-space", api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 이슈 생성
issue = client.create_issue({
    "projectId": "123",
    "summary": "New task",
    "description": "Description"
})
```

##ライセンス

MIT License