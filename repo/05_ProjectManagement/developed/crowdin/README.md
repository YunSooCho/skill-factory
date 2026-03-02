#Crowdin APIクライアント

Crowdin用のPython APIクライアント。ローカライズ管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from crowdin import CrowdinClient, CrowdinError

client = CrowdinClient(access_token="YOUR_ACCESS_TOKEN")

# 프로젝트 조회
projects = client.list_projects()

# 번역 상태 조회
status = client.get_translation_status("project_id")
```

##ライセンス

MIT License