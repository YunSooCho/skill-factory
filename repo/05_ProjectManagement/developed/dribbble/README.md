#Dribbble APIクライアント

Dribbble用のPython APIクライアントです。デザインプラットフォーム機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from dribbble import DribbbleClient, DribbbleError

client = DribbbleClient(access_token="YOUR_ACCESS_TOKEN")

# 샷 조회
shots = client.get_shots()

# 프로젝트 조회
projects = client.get_projects()
```

##ライセンス

MIT License