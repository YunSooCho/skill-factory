#Connecteam APIクライアント

Connecteam用のPython APIクライアントです。人材管理機能を提供します。

## インストール

```bash
pip install requests
```

##使用法

```python
from connecteam import ConnecteamClient, ConnecteamError

client = ConnecteamClient(api_token="YOUR_API_TOKEN")

# 직원 조회
employees = client.get_employees()

# 교대 생성
shift = client.create_shift({"employeeId": "123", "start": "2024-01-01T09:00:00Z"})
```

##ライセンス

MIT License