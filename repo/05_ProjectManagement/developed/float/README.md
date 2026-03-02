# Float API クライアント

Float用のPython APIクライアントです。人材スケジューリング機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from float import FloatClient, FloatError

client = FloatClient(api_token="YOUR_API_TOKEN")

# 프로젝트 조회
projects = client.get_projects()

# 스케줄 조회
schedules = client.get_schedules("2024-01-01", "2024-01-31")
```

##ライセンス

MIT License