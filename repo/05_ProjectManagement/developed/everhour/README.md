#Everhour APIクライアント

Everhour用のPython APIクライアント。時間追跡機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from everhour import EverhourClient, EverhourError

client = EverhourClient(api_key="YOUR_API_KEY")

# 프로젝트 조회
projects = client.get_projects()

# 시간 기록 생성
entry = client.create_time_entry({"task": "123", "hours": 2.5})
```

##ライセンス

MIT License